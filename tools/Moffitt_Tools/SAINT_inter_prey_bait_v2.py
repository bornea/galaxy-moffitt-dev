<tool id="SAINT_inter_prey_bait_v2" name="SAINT pre-processing">
  <description></description>
  <command interpreter="python">SAINT_inter_prey_bait_v2.py $input $inter_output $bait_output $prey_output</command>
  <inputs>
    <param format="dat" name="input" type="data" label="Input File"/>
  </inputs>
  <outputs>
    <data format="txt" name="inter_output" label="Inter File"/>    
    <data format="txt" name="bait_output" label="Bait File" />
    <data format="txt" name="prey_output" label="Prey File" />
  </outputs>
  <stdio>
    <regex match="error"
	   source="stdout"
           level="fatal"
           description="Unknown error"/>
  </stdio> 

  <tests>
    <test>
      <param name="input" value="fa_gc_content_input.fa"/>
      <output name="out_file1" file="fa_gc_content_output.txt"/>
    </test>
  </tests>
  <help>
  </help>
</tool>