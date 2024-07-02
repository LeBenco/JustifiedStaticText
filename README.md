# Justified Static Text
Subclass of `wx.StaticText` that applies double justification to the label,
i.e. the text will be aligned both horizontally and vertically. All options
from StaticText are applied, plus an extra option allowing to specify line
spacing (as a factor applied to the current font size).

Justification is greedily determined, meaning that once the word spacing
of a line is set, it will not be changed, even if this results in better
justification for subsequent lines. Here's the algorithm used:
<code>
|For each line in the label: 
|&nbsp;&nbsp;&nbsp;&nbsp;Compute the width of the line considering regular word spacing
|&nbsp;&nbsp;&nbsp;&nbsp;If line width < available width:
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;Draw the line without justification
|&nbsp;&nbsp;&nbsp;&nbsp;Else: 
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;Split the line into multiple inner lines that fit
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;the available width considering regular word spacing
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;For each inner line except for the last one:
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;Draw the line with double justification
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;Draw the last inner line without justification
</code>      


Drawing a line of text with double justification is done with this
algorithm, using floating-point precision to ensure precise positioning:
<code>
Width for justification = (available width - total words width)
Single space width = Width for justification / (# of word - 1)
Draw each word using the calculated space width
</code>
