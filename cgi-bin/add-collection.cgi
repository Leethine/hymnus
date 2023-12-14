#!/usr/bin/perl

use strict;
use warnings;

sub filter_input {
  my $input = shift;
  my @plain = split(" ", $input);
  @plain= grep { $_ ne '' } @plain;
  my $out = join(' ', @plain);
  return $out;
}

my $CONTENTPATH="/var/sanctus_db/collection/";

# Read in text
$ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;

my $buffer;

if ($ENV{'REQUEST_METHOD'} eq "GET") {
   $buffer = $ENV{'QUERY_STRING'};
}

# Split information into name/value pairs
my @pairs = split(/&/, $buffer);

my %FORM;
foreach my $pair (@pairs) {
   my ($name, $value) = split(/=/, $pair);
   $value =~ tr/+/ /;
   $value =~ s/%(..)/pack("C", hex($1))/eg;
   $FORM{$name} = $value;
}

my $title = $FORM{"collection-title"};
my $subtitle = $FORM{"collection-subtitle"};
my $subsubtitle = $FORM{"collection-subsubtitle"};
my $composer = $FORM{"related-composer"};
my $opus = $FORM{"collection-opus"};
my $comment = $FORM{"collection-comment"};

# Filter the input
$title = filter_input($title);
$subtitle = filter_input($subtitle);
$subsubtitle = filter_input($subsubtitle);
$composer = filter_input($composer);
$opus = filter_input($opus);

print "Content-type:text/html\r\n\r\n";
print "<html>";
print "<head>";
print "<title>Created!</title>";
print "</head>";
print "<body>";
print "<h3>Creating new collection... Title:</h3><br><br>";
print "<h3>$title</h3><br>";
print "<h4>Subtitle: $subtitle</h4><br>";
print "<h4>Subsubtitle: $subsubtitle</h4><br>";
print "<h4>Opus: $opus</h4><br>";
print "<h4>Composer: $composer</h4><br>";
print "<p><b>Comments:</b> $comment</p><br>";

my $digest = $title . "\n" . $subtitle . "\n" . $subsubtitle . "\n" . $composer . "\n" . $opus . "\n" . $comment . "\n";

my $randnumber = rand();
$randnumber =~ s/\.//;
my $tempfile = $randnumber . ".temp";

open(FH, '>', $CONTENTPATH . $tempfile);
print FH $digest;
close(FH);

system("new_collection.sh " . $tempfile);
my $indexhtml = "http://" . $ENV{'HTTP_HOST'} . "/index.html";
my $collectionhtml = "http://" . $ENV{'HTTP_HOST'} . "/content/collections.html";

print "<h3>New collection created.</h3><br>";
print qq(<h3>&#11148; <a href="$indexhtml">Go back to main page</a></h3>);

system("perl /usr/local/bin/update_collection_page.pl");

print qq(<h3>&#8678; <a href="$collectionhtml">Go back to collection list</a></h3>);
print "</body>";
print "</html>";

1;