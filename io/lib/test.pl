use IO::Async::Loop;
use IO::Termios;
use Overland::IO::Protocol::ESPA444;
use IO::Handle;

use strict;
use warnings;

my $loop = IO::Async::Loop->new;

my $port = IO::Termios->open ($ARGV[0]) or die "$!";
#open my $fd,"+<",$ARGV[0];
#my $port = IO::Handle->new_from_fd ($fd,"w+");
#$port->setbaud(9600);
#$port->setcsize (8);
#$port->setparity ('n');
#$port->setstop (1);
#system("stty","-F",$ARGV[0],"-clocal");

stty ($ARGV[0],9600);

my $protocol = Overland::IO::Protocol::ESPA444->new (
  handle => $port,
);

$loop->add ($protocol);

$loop->run;

exit;

sub stty {
  my ($device,$baud) = @_;
 
  system ("stty","-F",$device,$baud,"-clocal","-cstopb","-parenb","cs8"); 
  
  return;
}

