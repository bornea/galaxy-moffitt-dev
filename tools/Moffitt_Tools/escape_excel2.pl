#!/usr/bin/perl -w

$date_abbrev_hash{'jan'} = 'january';
$date_abbrev_hash{'feb'} = 'february';
$date_abbrev_hash{'mar'} = 'march';
$date_abbrev_hash{'apr'} = 'april';
$date_abbrev_hash{'may'} = 'may';
$date_abbrev_hash{'jun'} = 'jun';
$date_abbrev_hash{'jul'} = 'july';
$date_abbrev_hash{'aug'} = 'august';
$date_abbrev_hash{'sep'} = 'september';
$date_abbrev_hash{'oct'} = 'october';
$date_abbrev_hash{'nov'} = 'november';
$date_abbrev_hash{'dec'} = 'december';

sub is_number
{
    return $_[0] =~ /^([+-]?)(?=[0-9]|\.[0-9])[0-9]*(\.[0-9]*)?([Ee]([+-]?[0-9]+))?$/;
}


sub has_text_month
{
    my $date_str = $_[0];
    my $abbrev;
    my $full;
    my $xor;
    my $prefix_length;

    $candidate = '';
    if ($date_str =~ /^([0-9]{1,4}[- \/]*)?([A-Za-z]{3,9})/)
    {
        $candidate = lc $2;
    }

    if ($candidate eq '')
    {
        return 0;
    }

    $abbrev = substr $candidate, 0, 3;
    $full = $date_abbrev_hash{$abbrev};

    # first three letters are not the start of a month
    if (!defined($full))
    {
        return 0;
    }

    # find common prefix
    $xor = "$candidate" ^ "$full";
    $xor =~ /^\0*/;
    $prefix_length = $+[0];
    
    # if the common prefix is the same as the full candidate, it is real
    if (length $candidate eq $prefix_length)
    {
        return 1;
    }
    
    return 0;
}


$escape_excel_most_flag = 1;
$escape_excel_paranoid_flag = 0;
$num_files = 0;

# read in command line arguments
for ($i = 0; $i < @ARGV; $i++)
{
    $field = $ARGV[$i];

    if ($field =~ /^-/)
    {
        if ($field eq '--paranoid')
        {
            if ($escape_excel_paranoid_flag == 0)
            {
                $escape_excel_paranoid_flag = 1;
            }
            else
            {
                $escape_excel_paranoid_flag = 0;
            }
        }
        else
        {
            printf "ABORT -- unknown option %s\n", $field;
            $syntax_error_flag = 1;
        }
    }
    else
    {
        if ($num_files == 0)
        {
            $filename = $field;
            $num_files++;
        }
    }
}

# default to stdin if no filename given
if ($num_files == 0)
{
    $filename = '-';
    $num_files = 1;
}

# print syntax error message
if ($num_files == 0 || $syntax_error_flag)
{
    printf "Syntax: escape_excel.pl [options] tab_delimited_text_file.txt\n";
    printf "   Options:\n";
    printf "      --paranoid   escape everything not a short-ish number\n";
    printf "                   WARNING -- Excel can take a LONG time to import\n";
    printf "                   text files where most fields are escaped...\n";
    printf "                   Copy / Paste Values can become near unusuable....\n";
    printf "\n";
    printf "   Input file must be tab-delimited.\n";
    printf "   Fields enclosed in \"\" will be recursively stripped of enclosing \"\", since\n";
    printf "    enclosing \"\" can lead to broken Excel behavior when escaped.\n";
    printf "   Fields with leading \" will then be recursively stripped, since\n";
    printf "    leading \" can cause truly unexpected behavior in Excel.\n";
    printf "\n";
    printf "   Defaults to escaping most (all ??) Excel mis-imported fields.\n";
    printf "   Escapes all cases I have encountered or imagined so far.\n";
    printf "   Escapes a few extra date-like formats that Excel does not consider dates.\n";
    printf "   Please send unhandled mis-imported field examples to Eric.Welsh\@moffitt.org\n";
    printf "    (I will try to fix it and send you a new version, if I have time)\n";
    printf "\n";
    printf "   Copy / Paste Values in Excel, after importing, to de-escape back into text.\n";
    printf "   Be sure to reformat to General before re-exporting to text, otherwise,\n";
    printf "    in some cases, Excel may destroy some data in the exported file.\n";
    exit(1);
}


$max_num_fields = 0;

if ($filename ne "-")
{
    # scan file for maximum number of fields
    open INFILE, "$filename" or die "can't open $filename\n";
    while(defined($line=<INFILE>))
    {
        @array = split /\t/, $line;
    
        if (@array > $max_num_fields)
        {
            $max_num_fields = @array;
        }
    }
    close INFILE;
}



# read in, escape, and print escaped lines
open INFILE, "$filename" or die "can't open $filename\n";
open(my $OUTFILE,'>',$ARGV[1]) or die "can't open '$ARGV[1]'\n";
while(defined($line=<INFILE>))
{
    # strip newline characters
    $line =~ s/[\r\n]+//g;

    @array = split /\t/, $line;
    if (@array > $max_num_fields)
    {
        $max_num_fields = @array;
    }
    
    for ($i = 0; $i < @array; $i++)
    {
        # remove start/end double quotes, since that will mess up escape stuff
        while ($array[$i] =~ /^\"/ && $array[$i] =~ /\"$/)
        {
            $array[$i] =~ s/^\"//;
            $array[$i] =~ s/\"$//;
        }
        
        # remove remaining leading quotes, since they mess up Excel in general
        while ($array[$i] =~ /^\"/)
        {
            $array[$i] =~ s/^\"//;
        }
    }
    
    # escape fields
    for ($i = 0; $i < @array; $i++)
    {
        # Strange but true -- 'text doesn't escape text properly in Excel,
        # it will not auto-strip the leading ' like it does when you type it
        # in a live spreadsheet.  "text" doesn't, either.
        # Oddly, ="text" DOES work, but violates all logical sanity....
        
        if ($escape_excel_paranoid_flag)
        {
          if (is_number($array[$i]))
          {
              # stop scientific notation for >11 digits before the decimal.
              # >11 is when it displays scientific notation in General format,
              # which can result in corruption when saved to text.
              # >15 would be the limit at which it loses precision internally.
              #
              # NOTE -- if there is a + or - at the beginning, this rule
              #         will not trigger.  Undecided if this is desired or not.
              #
              if ($array[$i] =~ /^[1-9][0-9]{11,}/)
              {
                  $array[$i] = sprintf "=\"%s\"", $array[$i];
              }
          }
          else
          {
              $array[$i] = sprintf "=\"%s\"", $array[$i];
          }
        }
        elsif ($escape_excel_most_flag)
        {
          # escape single quote at beginning of line
          if ($array[$i] =~ /^'/)
          {
              $array[$i] = sprintf "=\"%s\"", $array[$i];
          }

          # prevent conversion into formulas
          elsif ($array[$i] =~ /^\=/)
          {
              $array[$i] = sprintf "=\"%s\"", $array[$i];
          }
          elsif (!is_number($array[$i]) && $array[$i] =~ /^\+/ &&
                 !($array[$i] =~ /^\+\+/))
          {
              $array[$i] = sprintf "=\"%s\"", $array[$i];
          }
          elsif (!is_number($array[$i]) && $array[$i] =~ /^\-/ &&
                 !($array[$i] =~ /^\-\-/))
          {
              $array[$i] = sprintf "=\"%s\"", $array[$i];
          }

          # keep leading zeroes
          elsif (is_number($array[$i]) &&
                 $array[$i] =~ /^0+[1-9]([0-9]+)?/)
          {
              $array[$i] = sprintf "=\"%s\"", $array[$i];
          }

          # stop scientific notation for >11 digits before the decimal.
          # >11 is when it displays scientific notation in General format,
          # which can result in corruption when saved to text.
          # >15 would be the limit at which it loses precision internally.
          #
          # NOTE -- if there is a + or - at the beginning, this rule
          #         will not trigger.  Undecided if this is desired or not.
          #
          elsif (is_number($array[$i]) &&
                 $array[$i] =~ /^[1-9][0-9]{11,}/)
          {
              $array[$i] = sprintf "=\"%s\"", $array[$i];
          }


          # check for time and/or date stuff
          else
          {
              $time = '';
              $date = '';
          
              # attempt to guess at how excel might autoconvert into time
              # allow letter/punctuation at end if it could be part of a date
              #  it would get too complicated to handle date-ness correctly,
              #  since I'm already resorting to negative look-ahead
              if ($array[$i] =~ /\b(([0-9]+\s+(AM|PM|A|P)|[0-9]+:[0-9]+(:[0-9.]+)?)(\s+(AM|PM|A|P))?)(?!([^-\/, 0-9ADFJMNOSadfjmnos]))/)
              {
                  $time = $1;
              }
              
              $strip_time = $array[$i];
              if ($time =~ /\S/)
              {
                  $strip_time =~ s/\Q$time\E//;
                  $strip_time =~ s/^\s+//;
                  $strip_time =~ s/\s+$//
              }

              # text date, month in the middle
              if ($strip_time =~ /\b([0-9]{1,4}[- \/]*Jan[A-Za-z]{0,6}([- \/]*[0-9]{1,4})?)\b/i ||
                  $strip_time =~ /\b([0-9]{1,4}[- \/]*Feb[A-Za-z]{0,6}([- \/]*[0-9]{1,4})?)\b/i ||
                  $strip_time =~ /\b([0-9]{1,4}[- \/]*Mar[A-Za-z]{0,6}([- \/]*[0-9]{1,4})?)\b/i ||
                  $strip_time =~ /\b([0-9]{1,4}[- \/]*Apr[A-Za-z]{0,6}([- \/]*[0-9]{1,4})?)\b/i ||
                  $strip_time =~ /\b([0-9]{1,4}[- \/]*May[A-Za-z]{0,6}([- \/]*[0-9]{1,4})?)\b/i ||
                  $strip_time =~ /\b([0-9]{1,4}[- \/]*Jun[A-Za-z]{0,6}([- \/]*[0-9]{1,4})?)\b/i ||
                  $strip_time =~ /\b([0-9]{1,4}[- \/]*Jul[A-Za-z]{0,6}([- \/]*[0-9]{1,4})?)\b/i ||
                  $strip_time =~ /\b([0-9]{1,4}[- \/]*Aug[A-Za-z]{0,6}([- \/]*[0-9]{1,4})?)\b/i ||
                  $strip_time =~ /\b([0-9]{1,4}[- \/]*Sep[A-Za-z]{0,6}([- \/]*[0-9]{1,4})?)\b/i ||
                  $strip_time =~ /\b([0-9]{1,4}[- \/]*Oct[A-Za-z]{0,6}([- \/]*[0-9]{1,4})?)\b/i ||
                  $strip_time =~ /\b([0-9]{1,4}[- \/]*Nov[A-Za-z]{0,6}([- \/]*[0-9]{1,4})?)\b/i ||
                  $strip_time =~ /\b([0-9]{1,4}[- \/]*Dec[A-Za-z]{0,6}([- \/]*[0-9]{1,4})?)\b/i)
              {
                  $temp = $1;
              
                  if (has_text_month($temp))
                  {
                      $date = $temp;
                  }
              }

              # text date, month first
              elsif ($strip_time =~ /\b(Jan[A-Za-z]{0,6}[- \/]*[0-9]{1,4}([- \/]+[0-9]{1,4})?)\b/i ||
                     $strip_time =~ /\b(Feb[A-Za-z]{0,6}[- \/]*[0-9]{1,4}([- \/]+[0-9]{1,4})?)\b/i ||
                     $strip_time =~ /\b(Mar[A-Za-z]{0,6}[- \/]*[0-9]{1,4}([- \/]+[0-9]{1,4})?)\b/i ||
                     $strip_time =~ /\b(Apr[A-Za-z]{0,6}[- \/]*[0-9]{1,4}([- \/]+[0-9]{1,4})?)\b/i ||
                     $strip_time =~ /\b(May[A-Za-z]{0,6}[- \/]*[0-9]{1,4}([- \/]+[0-9]{1,4})?)\b/i ||
                     $strip_time =~ /\b(Jun[A-Za-z]{0,6}[- \/]*[0-9]{1,4}([- \/]+[0-9]{1,4})?)\b/i ||
                     $strip_time =~ /\b(Jul[A-Za-z]{0,6}[- \/]*[0-9]{1,4}([- \/]+[0-9]{1,4})?)\b/i ||
                     $strip_time =~ /\b(Aug[A-Za-z]{0,6}[- \/]*[0-9]{1,4}([- \/]+[0-9]{1,4})?)\b/i ||
                     $strip_time =~ /\b(Sep[A-Za-z]{0,6}[- \/]*[0-9]{1,4}([- \/]+[0-9]{1,4})?)\b/i ||
                     $strip_time =~ /\b(Oct[A-Za-z]{0,6}[- \/]*[0-9]{1,4}([- \/]+[0-9]{1,4})?)\b/i ||
                     $strip_time =~ /\b(Nov[A-Za-z]{0,6}[- \/]*[0-9]{1,4}([- \/]+[0-9]{1,4})?)\b/i ||
                     $strip_time =~ /\b(Dec[A-Za-z]{0,6}[- \/]*[0-9]{1,4}([- \/]+[0-9]{1,4})?)\b/i)
              {
                  $temp = $1;

                  if (has_text_month($temp))
                  {
                      $date = $temp;
                  }
              }

              # possibly a numeric date
              elsif ($strip_time =~ /\b([0-9]{1,4}[- \/]+[0-9]{1,2}[- \/]+[0-9]{1,2})\b/ ||
                     $strip_time =~ /\b([0-9]{1,2}[- \/]+[0-9]{1,4}[- \/]+[0-9]{1,2})\b/ ||
                     $strip_time =~ /\b([0-9]{1,2}[- \/]+[0-9]{1,2}[- \/]+[0-9]{1,4})\b/ ||
                     $strip_time =~ /\b([0-9]{1,2}[- \/]+[0-9]{1,4})\b/ ||
                     $strip_time =~ /\b([0-9]{1,4}[- \/]+[0-9]{1,2})\b/)
              {
                  $date = $1;
              }
              
              # be sure that date and time anchor the ends
              # mix of time and date
              if ($time =~ /\S/ && $date =~ /\S/)
              {
                  if ($array[$i] =~ /^\Q$time\E(.*)\Q$date\E$/ ||
                      $array[$i] =~ /^\Q$date\E(.*)\Q$time\E$/)
                  {
                      $middle = $1;

                      # allow blank
                      # allow for purely whitespace
                      # allow for a single hyphen, slash, comma
                      #  allow for multiple spaces before and/or after
                      if ($middle eq '' ||
                          $middle =~ /^\s+$/ ||
                          $middle =~ /^\s*[-\/,]\s*$/)
                      {
                          $array[$i] = sprintf "=\"%s\"", $array[$i];
#printf STDERR "BOTH\t%s\t\t%s\t%s\n", $time, $date, $array[$i];
                      }
                  }
              }
              # only time
              elsif ($time =~ /\S/)
              {
                  if ($array[$i] =~ /^\Q$time\E$/)
                  {
                      $array[$i] = sprintf "=\"%s\"", $array[$i];
#printf STDERR "TIME\t%s\t%s\n", $time, $array[$i];
                  }
              }
              # only date
              elsif ($date =~ /\S/)
              {
                  if ($array[$i] =~ /^\Q$date\E$/)
                  {
                      $array[$i] = sprintf "=\"%s\"", $array[$i];
#printf STDERR "DATE\t%s\t%s\n", $date, $array[$i];
                  }
              }
          }
        }
    }
    
    # make the new escaped line
    $line_escaped = join "\t", @array;
    
    # print it
    printf $OUTFILE "%s\n", $line_escaped;
}
close INFILE;
close $OUTFILE;
