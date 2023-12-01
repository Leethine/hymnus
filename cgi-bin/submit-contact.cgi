#!/usr/bin/perl

local ($buffer, @pairs, $pair, $name, $value, %FORM);
$ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;

if ($ENV{'REQUEST_METHOD'} eq "POST") {
   $buffer = $ENV{'QUERY_STRING'};
}

print "Content-type:text/html\r\n\r\n";
print "<html>";
print "<head>";
print "<title>Hello - Second CGI Program</title>";
print "</head>";
print "<body>";
print "<h2>Hello $buffer Second CGI Program</h2>";
print "</body>";
print "</html>";

1;