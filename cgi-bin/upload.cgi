#!/usr/bin/perl
use CGI;
use strict;
use warnings;

my $CONTENTDIR="/var/sanctus_db/score";
my $query = new CGI;

my $upload_filename = $query->param("work-score");
my $title = $query->param("work-title");
my $opus = $query->param("work-opus");
my $instrument = $query->param("work-instrument");

my $upload_filehandle = $query->upload("work-score");
open(UPLOADFH, '>', "$CONTENTDIR" . "/" . "test.txt");
while ( <$upload_filehandle> ) {
  print UPLOADFH;
}
close(UPLOADFH);

print "Content-type:text/html\r\n\r\n";
print "<html>";
print "<head>";
print "<title>Created!</title>";
print "</head>";
print "<body>";
print "</body>";
print "</html>";