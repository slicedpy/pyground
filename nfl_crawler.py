import urllib2
from bs4 import BeautifulSoup

# response = urllib2.urlopen("http://www.nfl.com/stats/categorystats?archive=false&conference=null&role=TM&offensiveStatisticCategory=TEAM_PASSING&defensiveStatisticCategory=null&season=2015&seasonType=REG&tabSeq=2&qualified=false&Submit=Go")
counter = 0



def strip_gaps(in_str):
    cut = str(in_str).replace("\n","")
    cut = cut.replace("										","")
    cut = cut.replace("									","")
    cut = cut.replace("							","")
    cut = cut.replace("							","")

    return cut

def get_data(address):
    response = urllib2.urlopen(address)
    html_doc = response.read()

    team = []
    season = []
    season_yds = []


    soup = BeautifulSoup(html_doc,'html.parser')

    table = ""
    for s in soup.table.find_all('td'):
        table += strip_gaps(s) + "\n"

    new_row_flag = 0
    table_soup = BeautifulSoup(table,'html.parser')

    data = table_soup.get_text().split("\n")


    for each in data:
        if new_row_flag == 21:
            season.append(team)
            new_row_flag = 0
            team = []
            
        team.append(str(each))
        new_row_flag += 1

    for each in season:
        #print each[9]
        season_yds.append(int(each[9].replace(",","")))

    return season_yds
    
    
all_yards = []
total_yards = 0
total_distance_yds = 0


for i in range(1932,2016):
    print "Now collecting the " + str(i) + " season."
    collect_season_yards = get_data("http://www.nfl.com/stats/categorystats?archive=false&conference=null&role=TM&offensiveStatisticCategory=TEAM_PASSING&defensiveStatisticCategory=null&season="+str(i)+"&seasonType=REG&tabSeq=2&qualified=false&Submit=Go")

    #print collect_season_yards
    
    for each in collect_season_yards:
        total_yards += each

##    print str(total_yards) + "\n"
##
##    #print "The " + str(i) + " season had " + str(total_yards)+ " total yards."
##
##    all_yards.append(total_yards)
##
##for each in all_yards:
##    total_distance_yds += each

#print "Through out history, the American football has traveled: " + str(total_distance_yds) + " yards."

total_distance_mi = float(int(total_yards)/ int(1760))

times_traveled_around = float(int(total_distance_mi) / int(24900))

print "This means an American football has traveled " + str(total_distance_mi) + " total miles."
print "Which means an American football has traveled, approximately, " + str(times_traveled_around) + " times around the world."
print "slicedpy"
