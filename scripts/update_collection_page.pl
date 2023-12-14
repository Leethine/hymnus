#!/usr/bin/perl

use strict;
use warnings;

my $CONTENTDIR="/var/sanctus_db/collection";

sub make_row {
  my $title = shift;
  my $composer = shift;
  my $hyperlink = shift;
  return qq(<tr><th><span><a href="$hyperlink">&#182;</a></span>&nbsp;&nbsp;$title</th><th>$composer</th></tr>\n);
}

system("rm /usr/local/apache2/htdocs/content/collections.html");
# TODO order by composer name
#system("rm /usr/local/apache2/htdocs/content/collections-alt.html");

my @catfiles = glob($CONTENTDIR . '/*.cat');
my $rows = "";

foreach (@catfiles) {
  my $thisfile = "$_";
  open(FH, '<', $thisfile);
  my $title = <FH>;
  my $subtitle = <FH>;
  my $subsubtitle = <FH>;
  my $composer = <FH>;
  my $opus = <FH>;
  $title = $title . " - " . $opus if ($opus ne "");

  $rows .= make_row("$title", "$composer", "#");
  close(FH);
}

open(FHT, '<', '/usr/local/apache2/hymnus_template/collections.html');
open(FH, '>', '/usr/local/apache2/htdocs/content/collections.html');

while(<FHT>) {
  my $line = "$_";
  if ($line =~ "<!--INSERT#HERE-->") {
     print FH $rows;
  }
  else {
    print FH $line;
  }
}

close(FHT);
close(FH);