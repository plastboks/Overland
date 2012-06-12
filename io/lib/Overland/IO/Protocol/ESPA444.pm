package Overland::IO::Protocol::ESPA444;

use Mo qw/default/;

use constant SOH => 1;
use constant STX => 2;
use constant ETX => 3;
use constant EOT => 4;
use constant ENQ => 5;
use constant ACK => 6;
use constant RS  => 30;
use constant US  => 31;

use constant LAST_CONTROL => 31;

extends qw/IO::Async::Protocol::Stream/;

has _tokens => (
    is      => 'ro',
    default => sub { [] },
);

has _is_slave => (
    is      => 'rw',
    default => sub { 0 },
);

has _is_passive => (
    is      => 'rw',
    default => sub { 0 },
);

has _is_selecting => (
    is      => 'rw',
    default => sub { 0 },
);

has address => (
    is      => 'rw',
    default => sub { 2 },
);

has strict => (
    is      => 'rw',
    default => sub { 1 },
);

sub on_read {
    my ($self,$bufref,$eof) = @_;

    push @{ $self->_tokens },unpack ("C*",$$bufref);

    $$bufref = '';

    while (1) {
      last unless $self->invoke_event (on_read_tokens => $self->_tokens);
    }

    return 0;
}

sub on_read_tokens {
    my ($self,$tokenref) = @_;

    print "Buffer: " . $self->_stringify_tokens (@$tokenref) . "\n";
    
    my $num_tokens = scalar @$tokenref;
    
    @$tokenref = $self->_parse_tokens (@$tokenref);
   
    return 1 if @$tokenref && @$tokenref < $num_tokens;
     
    return 0;
}

sub write_token {
    my ($self,$token) = @_;

    print "Output: " . $self->_stringify_tokens ($token) . "\n";    
    
    return $self->write (pack ("C",$token));
}

sub _parse_tokens {
    my ($self,@tokens) = @_;
    
    return () unless @tokens;

    if ($tokens[0] == EOT) {
        $self->_reset;
        
        shift @tokens;
    } elsif ($self->_is_passive) {
        shift @tokens while $tokens[0] != EOT;
    } else {    
        if ($self->_is_slave) {
            return $self->_parse_slave_tokens (@tokens);
        } else {
            return $self->_parse_waiting_tokens (@tokens);
        }
    }
    
    return @tokens;
}

sub _parse_waiting_tokens {
    my ($self,@tokens) = @_;
   
    if ($self->_is_selecting) {
      return $self->_parse_select (@tokens);
    } else {
      return $self->_parse_poll (@tokens);
    }
}

sub _parse_poll {
    my ($self,@tokens) = @_;

    return @tokens if @tokens < 2;
        
    my ($address,$enq) = splice @tokens,0,2;
    
    if ($enq == ENQ) {
        if ($self->_is_my_address ($address)) {
            $self->write_token (EOT);
        } else {
            print "-> Awaiting select\n";
        
            $self->_is_selecting (1);
        }
    } else {
        $self->_throw ("Expected poll sequence");
    }
    
    return @tokens;
}

sub _parse_select {
    my ($self,@tokens) = @_;
   
    return @tokens if @tokens < 2;
    
    my ($address,$enq) = splice @tokens,0,2;
   
    if ($enq == ENQ) {
        if ($self->_is_my_address ($address)) {
            print "-> Becoming slave\n"; 
        
            $self->_is_slave (1);
        
            $self->write_token (ACK);
        } else {
            print "-> Becoming passive\n";
            
            $self->_is_passive (1);
        }
    } else {
        $self->_throw ("Expected select sequence");
    }
    
    return;
}

sub _parse_slave_tokens {
    my ($self,@tokens) = @_;

    if ($tokens[0] == SOH) {
        return $self->_parse_data_block (@tokens);
    } else {
        $self->_throw ("Expected data sequence");
    }
}

sub _parse_data_block {
    my ($self,@tokens) = @_;

    my $complete_block = 0;
    
    for (my $i = 0; $i != @tokens; $i++) {
        if ($tokens[$i] == ETX && exists $tokens[$i+1]) {
            $complete_block = 1;
        }
    }
    
    return @tokens unless $complete_block;

    $self->write_token (ACK);
         
    return ();
}

sub _reset {
    my ($self) = @_;

    print "-> Resetting\n";
        
    $self->_is_slave (0);
    
    $self->_is_passive (0);
    
    $self->_is_selecting (0);
    
    return;
}

sub _is_my_address {
    my ($self,$token) = @_;
  
    return 1 if pack ("C",$token) == $self->address;
    
    return 0;
}

sub _throw {
    my ($self,$message) = @_;
    
    die "Error: $message (Got " . $self->_stringify_tokens (@{ $self->_tokens }) . ")\n";
}

my %token_names = (
    1  => "SOH",                                          
    2  => "STX",                                          
    3  => "ETX",                                          
    4  => "EOT",                                          
    5  => "ENQ",                                          
    6  => "ACK",                                          
    30 => "RS",     
    31 => "US",       
);

sub _stringify_tokens {
    my ($self,@tokens) = @_;

    my @prettified_tokens;
    
    foreach my $token (@tokens) {
        if (exists $token_names{ $token }) {
            push @prettified_tokens,$token_names{ $token };
        } elsif ($token > LAST_CONTROL) {
            push @prettified_tokens,"'" . chr ($token) . "'";
        } else {
            push @prettified_tokens,$token;
        }
    }
        
    return "[ " . join (', ',@prettified_tokens) . " ]";
}

1;

