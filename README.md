# Justified Static Text
Subclass of `wx.StaticText` that applies double justification to the label,
i.e. the text will be aligned both horizontally and vertically. All options
from StaticText are applied, plus an extra option allowing to specify line
spacing (as a factor applied to the current font size).

Justification is greedily determined, meaning that once the word spacing
of a line is set, it will not be changed, even if this results in better
justification for subsequent lines. Here's the algorithm used:
<code>
&nbsp;&nbsp;&nbsp;&nbsp;For each line in the label: 
        Compute the width of the line considering regular word spacing
        If line width < available width:
            Draw the line without justification
        Else: 
            Split the line into multiple inner lines that fit the available
                width considering regular word spacing
            For each inner line except for the last one:
                Draw the line with double justification
            Draw the last inner line without justification
      </code>      


Drawing a line of text with double justification is done with this
algorithm, using floating-point precision to ensure precise positioning:
    Width for justification = (available width - total words width)
    Single space width = Width for justification / (# of word - 1)
    Draw each word using the calculated space width
