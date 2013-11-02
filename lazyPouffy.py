import sublime, sublime_plugin

class LazyPouffyCommand(sublime_plugin.TextCommand):

	def run(self, edit):

		select =self.view.sel()[0].begin()
		current_line = self.view.rowcol(select)
		dupText =""
		found = False
		row = current_line[0]
		beginCount = 0
		endCount = 0
		
		for i in reversed(range( 0, row)):
			lineRegion =  self.view.text_point(i, 0)
			line = self.view.full_line(lineRegion)
			text = self.view.substr(line)
			text = text.strip()

			if text:
				if text[-1] == "}":
					endCount = endCount+1

				if text[-1] == "{" :
					beginCount = beginCount+1
					
				if endCount > 0 and beginCount == endCount:					
					found = True

				if found:	
					if text[-1] == "}" or text[-1] == ';' or text[-1] == '/':
						break
					dupText = text+ '\n' +dupText

		if dupText and found:
			dupText = dupText.replace('{','').strip()
			self.view.insert(edit, select, dupText+'{}')
			self.view.sel().clear()
			self.view.sel().add(sublime.Region(select + len(dupText)))
