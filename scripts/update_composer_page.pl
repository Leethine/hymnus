#!/usr/bin/perl

use strict;
use warnings;

my $CONTENTDIR="/var/sanctus_db/composer";

sub make_row {
  my $name = shift;
  my $year = shift;
  my $hyperlink = shift;
  return qq(<tr><th><span><a href="$hyperlink">&#182;</a></span>&nbsp;&nbsp;$name</th><th>$year</th></tr>\n);
}

system("rm /usr/local/apache2/htdocs/content/composers.html");
# TODO chronological order
#system("rm /usr/local/apache2/htdocs/content/composers-alt.html");

my @catfiles = glob($CONTENTDIR . '/*.cat');
my $rows = "";

foreach (@catfiles) {
  my $thisfile = "$_";
  my @catfilename = split("/", $thisfile);
  my $code = $catfilename[-1] =~ s/.cat//r;

  open(FH, '<', $thisfile);
  my $fullname = <FH>;
  my $firstname = <FH>;
  my $lastname = <FH>;
  my $byear = <FH>;
  my $dyear = <FH>;
  $rows .= make_row("$fullname", "($byear - $dyear)", "../../cgi-bin/composer.cgi?$code");
  close(FH);
}

open(FHT, '<', '/usr/local/apache2/hymnus_template/composers.html');
open(FH, '>', '/usr/local/apache2/htdocs/content/composers.html');

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
