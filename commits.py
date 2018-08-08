import json
import os

class commits(object):

    def __init__(self, fileName):
        self.fileName = fileName
    
    def read_json_file(self):
        with open(self.fileName, "r") as f:
            file_data = f.read()
            data = json.loads(file_data)
        return data

    def lines_of_code_by_author(self, name):
        data = self.read_json_file()
		
		# filter data by author name
        authorData = filter(lambda x: x.get('committer', None) == name, data)

        # get all projects for the author
        projects = map(lambda x: x.get('project', ''), authorData)
        
        # filter projects to remove empty values
        projects = filter(lambda x: x is not '', projects)
        
        # put projects in a "set" to remove duplicate values
        projects = list(set(projects))
        
        # get sum of all loc Added 
        locAdded = reduce(lambda x, y: x + getLOC(y,'added'), authorData, 0)
        
        # get sum of all loc Deleted 
        locDeleted= reduce(lambda x, y: x + getLOC(y,'deleted'), authorData, 0)
        
        # get commit with most modified loc
        largestCommit = reduce(lambda x, y : x if getLOC(x,'added') + getLOC(x,'deleted') 
        	> getLOC(y,'added') + getLOC(y,'deleted') else y, authorData,0)
        
        # prepare the result dictionary
        resDict = {}
        resDict['committer'] = name
        resDict['projectsWorkedOn'] = projects
        resDict['locAdded'] = locAdded
        resDict['locDeleted'] = locDeleted
        # don't set 'mostLinesModifiedOn' if no loc added or deleted by author or 
        # no date exists in input data
        if locAdded + locDeleted > 0 and 'date' in largestCommit:
            resDict['mostLinesModifiedOn'] = largestCommit['date']
        return resDict
        
       
def getLOC( commit, locType ):
    assert locType == 'added' or locType == 'deleted'
    # if input values doesn't exists return 0
    if commit and 'loc' in commit:
        return commit['loc'].get(locType, 0)
    return 0

if __name__ == "__main__":

    json_file = os.getcwd() + "/" +"data.json" 
    
    c = commits(json_file)
    print c.lines_of_code_by_author("john")
    print c.lines_of_code_by_author("mary")
    print c.lines_of_code_by_author("jack")
    print c.lines_of_code_by_author("chaya")