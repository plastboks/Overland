use IO::Termios;
use IO::Async::Loop;
use IO::Async::Stream;
use IO::Async::Protocol::LineStream;

use strict;
use warnings;

my $device_name = shift;

die "Specify device" unless defined $device_name;

my $device = IO::Termios->open ($device_name) or die "Cannot open device";

$device->setbaud(115200);
$device->setcsize(8);
$device->setparity('n');
$device->setstop(1);

my $loop = IO::Async::Loop->new;

my $protocol = IO::Async::Protocol::LineStream->new (
  handle => $device,
  on_read_line => sub {
    my ($self,$line) = @_;

    if ($line =~ "EOT 1 ENQ 2 ENQ") {
      $self->write_line ("ACK");
    } else {
      $self->write_line ("You didn't say hello!");
    }

    return;
  },
);

$loop->add ($protocol);

$loop->run;
