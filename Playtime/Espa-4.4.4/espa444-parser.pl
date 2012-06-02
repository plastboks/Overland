#espa test

use 5.012;
use strict;
use warnings;


my $espaString = "SOH 1 STX 1 US 4 3 9 2 RS 2 US 1 SPACE L e i l SPACE 1 RS 3 US 4 RS 4 US 3 ETX CR";
my @espaSplit = split " ", $espaString;

my $espaHeader = 0;
my $espaCallAddress = 0;
my $espaDisplayMessage = 0;
my $espaBeepCoding = 0;
my $espaCallType = 0;
my $espaNumberTransmission = 0;
my $espaPriority = 0;
my $espaCallStatus = 0;


sub espaPartJoin{
    my ($list) = (@_);
    shift @$list;
    my @record;
    while ($$list[0] ne "RS" && $$list[0] ne "ETX"){
        my $item = shift(@$list);
        if ($item eq "SPACE"){
            push @record, " ";
        } else {
            push @record, $item;
        }
    }
    return join "", @record;
}

while (my $item = shift @espaSplit) {
    given($item) {
        when("SOH"){
            $espaHeader = shift @espaSplit;
            shift @espaSplit; #skip "STX"
        }
        when("1"){
            $espaCallAddress = espaPartJoin(\@espaSplit);
        }
        when("2"){
            $espaDisplayMessage = espaPartJoin(\@espaSplit);
        }
        when("3"){
            $espaBeepCoding = espaPartJoin(\@espaSplit);
        }
        when("4"){
            $espaCallType = espaPartJoin(\@espaSplit);
        }
        when("5"){
            $espaNumberTransmission = espaPartJoin(\@espaSplit);
        }
        when("6"){
            $espaPriority = espaPartJoin(\@espaSplit);
        }
        when("7"){
            $espaCallStatus = espaPartJoin(\@espaSplit);
        }
        when("ETX"){
            #do nothing for now... checksum calculation is going to happend here.
        }
    }
}

print "Header: " . $espaHeader . "\n";
print "Call Address: " . $espaCallAddress . "\n";
print "Display Message: " . $espaDisplayMessage . "\n";
print "Beep Coding: " . $espaBeepCoding . "\n";
print "Call Type: " . $espaCallType . "\n";
print "Number of transmissions: " . $espaNumberTransmission . "\n";
print "Priority: " . $espaPriority . "\n";
print "Call Status: " . $espaCallStatus . "\n";




