# Justified Static Text
Python subclass of `wx.StaticText` that applies double justification to the label, i.e. the text will be aligned vertically on both sides. All options from StaticText are applied, plus an extra option allowing to specify line
spacing (as a factor applied to the current font size).

Please note that this is a proof of concept and may require adaptation to meet specific needs. 

Justification is greedily determined, meaning that once the word spacing of a line is set, it will not be changed, even if this results in better justification for subsequent lines. Here's the algorithm used:
```
For each line in the label: 
│    Compute line width using regular word spacing
│    If line width ≤ available width:
│    │    Draw the line without justification
│    Else:
│    │    Split the line into inner lines that fit available width using regular word spacing
│    │    For each inner line except the last one:
│    │    │    Draw the line with double justification
│    │    Draw the last inner line without justification
```

Note that in reality, the algorithm is a little more elaborate, since the justification of the last (or only, for short lines) inner line can be optionally set.

Drawing a line of text with double justification is done with this algorithm, using floating-point precision to ensure precise positioning:<br>
```
                      (available width - total words width)
single space width 🡨 ⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺
                                (# of words-1)
                                
If single space width > maximum allowed space width:
│    single space width 🡨 maximum allowed space width

Draw each word using the calculated single space width
```
`maximum allowed space width` is defined proportionnaly to the regular width of a space character.

Here is a simple example using `JustifiedStaticText`:
```python
if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None, title="Justified Static Text Demo", size=(400, 300))
    panel = wx.Panel(frame)

    text = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed  do "
            "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut "
            "enim ad minim veniam, quis nostrud exercitation  ullamco laboris "
            "nisi ut aliquip ex ea  commodo consequat. Duis aute irure dolor "
            "in reprehenderit  in voluptate velit esse cillum dolore eu "
            "fugiat nulla pariatur. Excepteur sint occaecat cupidatat non "
            "proident,  sunt in culpa qui officia deserunt mollit anim id est "
            "laborum."
    )

    justified_text = JustifiedStaticText(panel, label=text)
    sizer = wx.BoxSizer(wx.VERTICAL)    
    sizer.Add(justified_text, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
    panel.SetSizer(sizer)

    frame.Show()
    app.MainLoop()
```

    

