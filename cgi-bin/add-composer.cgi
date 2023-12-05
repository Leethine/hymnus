#!/usr/bin/perl

use strict;
use warnings;

my $CONTENTPATH="/var/sanctus_db/composer/";

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

my $fullname = $FORM{"full-name"};
my $lastname = $FORM{"last-name"};
my $firstname = $FORM{"first-name"};
my $byear = $FORM{"born-year"};
my $dyear = $FORM{"died-year"};

$byear = "?" unless ($byear =~ /[0-9]{2,4}/);
$dyear = "?" unless ($dyear =~ /[0-9]{2,4}/);

print "Content-type:text/html\r\n\r\n";
print "<html>";
print "<head>";
print "<title>Created!</title>";
print "</head>";
print "<body>";
print "<h3>Creating new composer...</h3><br><br>";
print "<h4>$fullname ($byear - $dyear)</h4><br>";
print "<h4>First Name: $firstname</h4><br>";
print "<h4>Last Name: $lastname</h4><br>";

my $digest = $fullname . "\n" . $lastname . "\n" . $firstname . "\n" . $byear . "\n" . $dyear . "\n";
my $randnumber = rand();
$randnumber =~ s/\.//;
my $tempfile = $randnumber . ".temp";

open(FH, '>', $CONTENTPATH . $tempfile);
print FH $digest;
close(FH);

system("new_composer.sh " . $tempfile);
my $indexhtml = "http://" . $ENV{'HTTP_HOST'} . "/index.html";

print "<h3>New composer created.</h3><br>";
print qq(<h3>&#9842; <a href="$indexhtml">Go back to main page</a></h3>);
print "</body>";
print "</html>";

1;