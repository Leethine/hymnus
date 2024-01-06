#!/usr/bin/perl

use strict;
use warnings;

# Read composer entry
my $CONTENTDIR="/var/sanctus_db/composer";
my $code = $ENV{'QUERY_STRING'};
my %composerinfo;

open(FH, '<', $CONTENTDIR . "/" . $code . ".cat");
$composerinfo{'FULLNAME'} = <FH>;
$composerinfo{'FIRSTNAME'} = <FH>;
$composerinfo{'LASTNAME'} = <FH>;
$composerinfo{'BORNYEAR'} = <FH>;
$composerinfo{'DIEDYEAR'} = <FH>;
$composerinfo{'HASHCODE'} = <FH>;
close(FH);

# Prepare html page
my $hostaddr = "http://" . $ENV{'HTTP_HOST'};

my $page_head = qq(
<!DOCTYPE html>
<html>
<head>
<title>Composer</title>
  <link rel="icon" type="image/x-icon" href="$hostaddr/icon.ico">
  <link rel="stylesheet" href="$hostaddr/styles.css">
</head>
<body>
);

my $page_menu = qq(
<ul>
  <li><a href="$hostaddr/home.html">Home</a></li>
  <li><a href="$hostaddr/content/composers.html">Composers</a></li>
  <li><a href="$hostaddr/content/collections.html">Collections</a></li>
  <li><a href="$hostaddr/about.html">About</a></li>
</ul>
);

my $page_add = qq(
<h3>$composerinfo{'FULLNAME'}</h3>
<h4>($composerinfo{'BORNYEAR'} - $composerinfo{'DIEDYEAR'})</h4>
<br>
<form action="upload.cgi" method="POST" enctype="multipart/form-data">
Title: <input type="text" name="work-title">
<br>
Opus: <input type="text" name="work-opus">
<br>
Instruments: <input type="text" name="work-instrument">
<br>
Code (do not modify): <input type="text" value="$code" readonly>
<br>
File to upload: <input type="file" name="work-score">
<input type="submit" name="submit" value="Submit">
</form>
);

my $page_content = qq(
);

my $page_end = qq(
</body>
</html>
);

print "$page_head";
print "$page_menu";
print "$page_content";
print "$page_add";
print "$page_end";
