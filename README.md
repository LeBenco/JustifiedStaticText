# Justified Static Text
Subclass of `wx.StaticText` that applies double justification to the label,
i.e. the text will be aligned both horizontally and vertically. All options
from StaticText are applied, plus an extra option allowing to specify line
spacing (as a factor applied to the current font size).

Justification is greedily determined, meaning that once the word spacing
of a line is set, it will not be changed, even if this results in better
justification for subsequent lines. Here's the algorithm used:
    For each line in the label: 
        Compute the width of the line considering regular word spacing
        If line width < available width:
            Draw the line without justification
        Else: 
            Split the line into multiple inner lines that fit the available
                width considering regular word spacing
            For each inner line except for the last one:
                Draw the line with double justification
            Draw the last inner line without justification
            


<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
<foreignObject width="100" height="100">
    <div xmlns="http://www.w3.org/1999/xhtml">
<div style="border-left: 1px solid black;padding-left:25px;margin:5px;">
    For each line in the label
    <div style="border-left: 1px solid black;padding-left:25px;margin:5px;">
        Compute the width of the line considering regular word spacing<br>
        If line width < available width
        <div style="border-left: 1px solid black;padding-left:25px;margin:5px;">
          Draw the line without justification<br>
        </div>
        Else:
        <div style="border-left: 1px solid black;padding-left:25px;margin:5px;">
          Split the line into multiple inner lines that fit the available width considering regular word spacing<br>
          For each inner line except for the last one
          <div style="border-left: 1px solid black;padding-left:25px;margin:5px;">
              Draw the line with double justification
          </div>
          Draw the last inner line without justification
        </div>
    </div>
</div>
    </div>
</foreignObject>
</svg>

Drawing a line of text with double justification is done with this
algorithm, using floating-point precision to ensure precise positioning:
    Width for justification = (available width - total words width)
    Single space width = Width for justification / (# of word - 1)
    Draw each word using the calculated space width
