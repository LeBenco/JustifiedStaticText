"""
MIT License

Copyright (c) 2024 Benjamin Cohen Boulakia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

################################################################################
############################ Justified Static Text  ############################

class JustifiedStaticText(wx.StaticText):
    """
    Subclass of `wx.StaticText` that applies double justification to the label,
    i.e. the text will be aligned vertically on both sides. All options from
    `wx.StaticText` are applied, plus an extra option allowing to specify line
    spacing (as a factor applied to the current font size).

    Justification is greedily determined, meaning that once the word spacing of
    a line is set, it will not be changed, even if this would result in better
    justification for subsequent lines. Here's the algorithm used:
    ```
    For each line in the label: 
    |    Compute the width of the line considering regular word spacing
    |    If line width < available width:
    |    |    Draw the line without justification
    |    Else:
    |    |    Split the line into inner lines that fit available width using
    |    |      regular word spacing
    |    |    For each inner line except the last one:
    |    |    |    Draw the line with double justification
    |    |    Draw the last inner line without justification
    ```

    Note that in reality, the algorithm is a little more, since the justification of
    the last (or only, for short lines) inner line can be optionally set.
    
    Drawing a line of text with double justification is done with this algorithm,
    using floating-point precision to ensure precise positioning:
    ```
    Width for justification = (available width - total words width)
    Single space width = Width for justification / (# of word - 1)
    If single space width > maximum allowed space width:
    |    single space width <- maximum allowed space width
    Draw each word using the calculated single space width
    ```
    `maximum allowed space width` is defined proportionnaly to the regular
    width of a space character.
    """
    
    def __init__(self, parent, line_spacing_factor=0,
                 non_breaking_spaces = True, justify_last_line = False,
                 max_space_width_factor= 1.6, *args, **kwargs):
        """
        Constructor.

        Parameters:
        * `parent`: wx parent widget.
        * `line_spacing_factor` (float): Factor applied to the current font size
            to compute line spacing. Default is 0.
        * `non_breaking_spaces` (bool): If True, common rules for non-breaking
            spaces are applied (e.g., forbid wrap after «). Default is True.
        * `justify_last_line` (bool): If True, the last line of text will be justified.
            Default is False.
        * `max_space_width_factor` (float): Maximum width factor for spaces when justifying.
            Default is 1.6.
        * `*args`: Additional positional arguments passed to wx.StaticText constructor.
        * `**kwargs`: Additional keyword arguments passed to wx.StaticText constructor.

        Note:
        The `style` parameter (either in args or kwargs) will always have
        `wx.ST_NO_AUTORESIZE` added to it. If `style` is not provided, it will
        be set to `wx.ST_NO_AUTORESIZE`.
        """
        self._nonBreakingSpaces = non_breaking_spaces
        
        sig = inspect.signature(wx.StaticText.__init__).parameters
        # Update style in args or kwargs with wx.ST_NO_AUTORESIZE
        if "style" in sig:
            args_list = list(args)
            style_index = list(sig).index("style")
            args_list[style_index] = args_list[style_index] | wx.ST_NO_AUTORESIZE
            args = tuple(args_list)
        else:
            kwargs["style"] = kwargs.get("style", 0) | wx.ST_NO_AUTORESIZE

        # Call parent constructor
        super().__init__(parent, *args, **kwargs)
        self._lineSpacingFactor = line_spacing_factor
        self._justifyLastLine = justify_last_line
        self._maxSpaceWidthFactor = max_space_width_factor
        self.Bind(wx.EVT_PAINT, self._OnPaint)

    def SetLabel(self, label):
        """
        Updates label. if `non_breaking_spaces` is set, spaces will be replaced
        with non-breaking spaces wherever relevant (ex: after «)
        
        * `label`: the new label
        """
        if self._nonBreakingSpaces:
            chars = [":", "\"", "'", ";", "«", "»"]
            for char in chars:
                label.replace(char+" ", char+u"\u00A0")

        super().SetLabel(label)

    def _OnPaint(self, event):
        """
        Callback for paint event. Draws the label
        
        * `event`: the paint event
        """

        # set up drawing context and clear widget
        dc = wx.BufferedPaintDC(self)
        dc.SetFont(self.GetFont())
        dc.SetTextForeground(self.GetForegroundColour())
        dc.SetTextBackground(self.GetBackgroundColour())
        
        dc.SetDeviceOrigin(self.GetScrollPos(wx.HORIZONTAL), self.GetScrollPos(wx.VERTICAL))
        dc.Clear()

        # each line is processed separately
        text = self.GetLabel()
        lines = text.split("\n")
        
        line_spacing = dc.GetFont().GetPointSize() * self._lineSpacingFactor
        y = 0
        richtext_width = self.GetClientSize()[0]
        for i, line in enumerate(lines):
            # the line is splitted into words in order to compute all subsets of
            # words that fit into the width
            words = line.split()
            line_width = dc.GetTextExtent(" ".join(words))[0]
            
            if line_width < richtext_width:
                # if the line fits into the container, it is drawn
                self._DrawJustifiedLine(dc, words, y, i == len(lines) - 1)
                
                # update y position for next line
                y += dc.GetTextExtent(" ".join(words))[1] + line_spacing
            else:
                # if the lines doesn't fit, it is splitted into several inner
                # lines according to the available width.
                
                # inner lines are built word by word and displayed as they go along
                start = 0
                while start < len(words):
                    # build current inner line with the remaining words, by
                    # counting how many words can be added without exceeding
                    # the available width
                    end = start
                    current_width = 0
                    while end < len(words) and dc.GetTextExtent(" ".join(words[start:end+1]))[0] <= richtext_width:
                        end += 1
                    
                    # display the current inner line
                    if end > start:
                        # most common case, when the inner line contains
                        # several words to display
                        self._DrawJustifiedLine(dc, words[start:end], y,
                                               end == len(words))
                        
                        # update y position for next line
                        y += dc.GetTextExtent(" ".join(words[start:end]))[1] + line_spacing
                        
                        # go to the beginning of the next inner line
                        start = end
                    else:
                        # specific case when there when the inner line contains
                        # only one word to display
                        self._DrawJustifiedLine(dc, [words[start]], y, True)

                        # update y position for next line
                        y += dc.GetTextExtent(words[start])[1] + line_spacing

                        # go to the beginning of the next inner line
                        start += 1
            
    def _DrawJustifiedLine(self, dc, words, y, is_last_line):
        """
        Draws a line of text with double justification.
        
        * `dc`: the context on which to draw text
        * `words`: the text, as a list of words
        * `y`: the vertical position to display the text
        * `is_last_line`: Boolean indicating whether the line is the last in
                          the block. If `True`, justification won't be applied
        """
        
        # compute width for all spaces between words
        total_width = sum(dc.GetTextExtent(word)[0] for word in words)
        available_width = self.GetClientSize()[0]
        extra_width = available_width - total_width

        # compute individual width of a space character
        num_spaces = len(words) - 1
        width_per_space = 0
        if num_spaces > 0:
            if is_last_line:
                if self._justifyLastLine:
                    width_per_space = min(
                        extra_width / num_spaces,
                        self._maxSpaceWidthFactor * dc.GetTextExtent(" ")[0])
                else:
                    width_per_space = dc.GetTextExtent(" ")[0]
            else:
                width_per_space = extra_width / num_spaces
        else:
            # specific case where there is only one word.
            width_per_space = 0

        # the x-position of words must be calculated with floating precision,
        # in order to achieve precise positioning. Integer precision usually
        # leads to lines that are not completely filled.
        x = 0.0

        # draw each word with computed space width between them
        for i, word in enumerate(words):
            # draw text
            dc.SetTextForeground(self.GetForegroundColour().Get(False))
            dc.SetTextBackground(self.GetBackgroundColour().Get(False))
            
            dc.DrawText(word, int(x), y)
            
            # update x position to the position of the next word
            x += dc.GetTextExtent(word)[0] + width_per_space
