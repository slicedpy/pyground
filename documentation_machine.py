import time
import os.path
import shutil



warnings = ['\n!!! - WARNING - !!!!','001','002','003']
warning_count = 0
exit_flag = False

q_prompts = ['Title: ','Prepared for: ','Prepared by: ','Last Revised Date: ','Iteration #: ']
default_ans = ['Report Title','Fruit of the Loom, Inc. - Analytics Group','Tiffanee C. Lang',time.strftime("%x"),'0']

dtl_prompts = ['Objective: ','Package details: ','Data: ','Technical Details: ', 'Additional Sources and Credits: ']
details_flag = False

fig_prompts = ['Graphic Figure?(full path to image): ','Include Code?(full path to script/txt): ']

document_dict = {}
default_dict = {'<type \'int\'>': -1,
                '<type \'str\'>':'N/A',
                'Title':'Default Report Title',
                'Prepared for':'Fruit of the Loom, Inc. - Analytics Group',
                'Prepared by':'Author Name',
                'Last Revised Date':time.strftime("%x"),
                'Iteration #':'0',
                'Objective':'N/A',
                'Package details':'N/A',
                'Data':'N/A',
                'Technical Details':'N/A',
                'Additional Sources and Credits':'N/A',
                'Graphic Figure?(full path to image)':'doc_imgs/no_fig.PNG',
                'Include Code?(full path to script/txt)':'No code to display'
                }

def get_ans(prompts,default=default_dict):
    marker = 0
    user_ans = []
    global warnings
    global warning_count
    global document_dict

    
    for each in prompts:
        get_ans = raw_input(each)
        
        if get_ans == '':
            user_ans.append(default_dict[str(each.replace(': ',''))])
            document_dict[str(each.replace(': ',''))] = str(default_dict[str(each.replace(': ',''))])
        else:
            user_ans.append(get_ans)
            document_dict[str(each.replace(': ',''))] = str(get_ans)
            
        marker += 1
        
    if len(user_ans) >= 4:
        try:
            int(user_ans[4])
        except ValueError:
            if prompts[4] == 'Iteration #: ':
                warnings[1] =("(001) Iteration corrected. Iterations must be an integer value.")
                warning_count += 1

    print "\n"

    return user_ans


def check_existence(checkfile,user_ans):
    global warnings
    global warning_count
    
    with open(checkfile,'r+') as docket:
        marker = 0
        for line in docket:
            if str(user_ans).strip() == str(line).strip():
                user_ans[4] = str(int(user_ans[4]) + 1)
                marker = -1
                
        if marker == -1:
            document_dict['Iteration #'] = str(user_ans[4])
            warnings[2] = "(002) Documentation already exist for " + str(user_ans[0] + ". Increasing the iteration tag to " + str(user_ans[4]))
            warning_count += 1
            marker = 0

        docket.write(str(user_ans)+"\n")
        details_flag = True

    # print "\nRecord Created.\n"



print open("de_title.txt","r").read()

while exit_flag == False:
    controller = raw_input(">>").lower()

    if controller == '' or controller == 'make doc' or controller == 'md':
        check_existence('doc_list.txt',get_ans(q_prompts,default_dict))
        get_ans(dtl_prompts,default_dict)
        get_ans(fig_prompts,default_dict)
        print "\nRecord Created.\n"


    error_cursor = 1
    write_flag = ''

    if warning_count > 0:
        print warnings[0]
        
    for each in warnings[1:]:
        error_code = "00" + str(error_cursor)
        try:
            warnings.index(error_code)
        except ValueError:
            print warnings[error_cursor]
            
        error_cursor += 1
            
    warnings = ['\n!!! - WARNING - !!!!','001','002','003']
    warning_count = 0
    print "\n"

    if os.path.isfile("C:\Python27\sliced_py\documentation\prj\/" + "tde_runtime_0.txt") == False:
        shutil.copy2("C:\Python27\sliced_py\documentation\prj\/tde_runtime_0.py","C:\Python27\sliced_py\documentation\prj\/tde_runtime_0.txt")


    with open('C:/Python27/sliced_py/documentation/prj/'+str(document_dict['Title']).replace(" ","_") + "_" + document_dict['Iteration #'] + '.htm' , 'w+') as site_document:
            try:
                project_code = open(document_dict['Include Code?(full path to script/txt)'],'r').read().replace('\n','</br>')
            except:
                project_code = document_dict['Include Code?(full path to script/txt)']
        
            markup = ''
            markup += '<style>font{font-family: \'Arial\';}</style>\n'
            markup += '<HTML><TITLE>' + document_dict['Title'] + '</TITLE>\n'
            markup += '<img src="doc_imgs/sp_doc_logo_0.PNG" width="42%"></br></br>\n'
            markup += '<font size="6">' + document_dict['Title'] + '</font></br></br>\n'
            markup += '<table border=0 width="100%"><tr><td valign="top" width="60%">\n'
            markup += '<b><font>Prepared for: </b>' + document_dict['Prepared for'] + '</br>\n'
            markup += '<b><font>Prepared by: </b>' + document_dict['Prepared by'] + '</br>\n'
            markup += '<b><font>Last Revised Date: </b>' + document_dict['Last Revised Date'] + '</br>\n'
            markup += '<b><font>Iteration #: </b>' + document_dict['Iteration #'] + '</br></br></br>\n'
            markup += '<b><font>Objective: </b>' + document_dict['Objective'] + '</br>\n'
            markup += '<b><font></br>Package details: </b>' + document_dict['Package details'] + '</br>\n'
            markup += '<b><font></br>Data: </b>' + document_dict['Data'] + '</br>\n'
            markup += '<b><font></br>Technical Details: </b>' + document_dict['Technical Details'] + '</br>'
            markup += '<b><font></br>Additional Sources and Credits: </b>' + document_dict['Additional Sources and Credits'] + '\n'
            markup += '</td><td><center><img src="'+ document_dict['Graphic Figure?(full path to image)'] +'"></center></td>\n'
            markup += '</tr><tr><td colspan=2></br><font size="Arial">' + project_code
            markup += '</font></td></tr><td colspan=2><p align="right"><img src="doc_imgs/small_wm.PNG" width=67 height=57></td></tr></table>\n'

            htm_doc = 'C:/Python27/sliced_py/documentation/prj/'+str(document_dict['Title']).replace(" ","_") + '.htm'
            site_document.write(markup)


    document_dict.clear()

