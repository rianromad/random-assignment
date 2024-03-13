import random
import streamlit as st
import numpy as np
import math
import pandas as pd
import warnings
warnings.filterwarnings('ignore')      


#FUNCTION
#-----------------------------------------------------------------------------------------------------------#

#single = satu orang satu task
#double = dua task bisa dikerjain satu orang

#jumlah task > jumlah orang

def assign_task(names,tasks,double=True):
    assign = {}
    tasks_remain = len(tasks)%len(names)

    if tasks_remain !=0:
        if double == True:
            double_candidate = names.copy()
            for i in range(tasks_remain):
                dc = random.choice(double_candidate)
                double_candidate.remove(dc)  
                names = names + [dc]  
        else:
            names = names + tasks_remain*['Not Assigned']  

    for t in tasks:
        c = random.choice(names)
        names.remove(c)
        assign.update({t:c})
    
    return pd.DataFrame({"Task":assign.keys(),"Name":assign.values()})

def assign_group(names, groups):
    remain = len(names)%groups 
    assign = {}

    if remain != 0:
        num_dummy = groups-remain
        names = names + num_dummy*['-'] 

    num = math.ceil(len(names)/groups)

    for i in range(1,groups+1):
        members = []
        for j in range(num):
            choice = random.choice(names)
            names.remove(choice)
            members.append(choice)
        assign.update({i:members})
    
    return pd.DataFrame(assign) 

def random_order(names):
    assign = {}
    order = np.arange(1,len(names)+1)
    for o in order:
        c = random.choice(names)
        names.remove(c)
        assign.update({c:o})
    return pd.DataFrame({"Name":assign.keys(),'Order':assign.values()})

#kalo dipencet lagi berkurang gituuu
def random_picker(names):
    return random.choice(names)

#toss coin
def toss():
    return random.choice(['Head','Tail'])

#roll dice
def roll():
    return random.choice(np.arange(1,7))

#pick number
def pick_number(low, up):
    return random.randint(low,up)

#MAIN PROGRAM
#-----------------------------------------------------------------------------------------------------------#
st.set_page_config(
    page_title="Random Assignment",
    page_icon="🎲",
    layout="wide"
)

#css file
with open('style.css')as f:
 st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

#create website title
st.header('Random Assignment App 🎲')
st.markdown('\n')

opt_col, dum = st.columns([3,5])
#app option 
list_opt = ['Assign Task', 'Assign Group', 'Assign Order', 'Random Picker', 'Toss a Coin', 'Roll a Dice', 'Pick Number' ]
with opt_col:
    opt = st.selectbox("Select Option:", options=list_opt)
    st.markdown("\n")

if opt=="Assign Task":
    name_col, task_col, double_col, assign_btn_col = st.columns([3,3,1,1])
    with name_col:
        #pisahkan dengan koma (,)
        name = st.text_input("Input your members here:","Andre, Bekti, Dodi")
        name = name.split(",")
    with task_col:    
        task = st.text_input("Input your tasks here:","Transport, Design and Documentary, Treasury")
        task = task.split(",")
    with double_col:
        double_opt = st.selectbox("Double Options:",[True,False])
    with assign_btn_col:
        assign_button = st.button("Assign")
    if assign_button:
        dwn_col, dum1, dum2 = st.columns([3,5,5])
        assign_df = assign_task(name,task,double_opt).set_index('Name')
        st.markdown('\n')
        st.dataframe(assign_df, use_container_width=True)
        #download data
        with dwn_col:
            csv = assign_df.to_csv().encode('utf-8')
            st.download_button(
            "📄 Download Result",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
            )
elif opt=="Assign Group":
    name_col,dum, group_col, dum2, assign_btn_col = st.columns([15,1,10,1,5])
    with name_col:
        name = st.text_input("Input your members here:","Andre, Bekti, Dodi, Eva, Farah, Ghani")
        name = name.split(",")
    with group_col:
        group = st.slider("Number of group:", min_value=1, max_value=len(name))
    with assign_btn_col:
        assign_button = st.button("Assign")
    if assign_button:
        dwn_col, dum1, dum2 = st.columns([3,5,5])
        assign_df = assign_group(name,group)
        st.dataframe(assign_df, use_container_width=True)

        #download data
        with dwn_col:
            csv = assign_df.to_csv().encode('utf-8')
            st.download_button(
            "📄 Download Result",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
            )
            
elif opt=="Assign Order":
    name_col, assign_btn_col = st.columns([3,1])
    with name_col:
        name = st.text_input("Input your members here:","Andre, Bekti, Dodi, Eva")
        name = name.split(",")
    with assign_btn_col:
        assign_button = st.button("Assign")
    if assign_button:
        dwn_col, dum1, dum2 = st.columns([3,5,5])
        assign_df = random_order(name).set_index('Name')
        st.markdown('\n')
        st.dataframe(assign_df, use_container_width=True)

        #download data
        with dwn_col:
            csv = assign_df.to_csv().encode('utf-8')
            st.download_button(
            "📄 Download Result",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
            )

elif opt=="Random Picker":
    name_col, assign_btn_col = st.columns([3,1])
    with name_col:
        name = st.text_input("Input your members here:","Andre, Bekti, Dodi, Eva")
        name = name.split(",")
    with assign_btn_col:
        assign_button = st.button("Assign")

    if assign_button:
        st.markdown('\n')
        sel_name = random_picker(name)
        st.info(f"Selected Members: {sel_name}")
        name.remove(sel_name)
        remains = ', '.join(name)
        st.success(f'Remaining Members: {remains}', icon='🤖')
            

elif opt=="Toss a Coin":
    toss_col, result_col,dum = st.columns([1,1,5])
    with toss_col:
        toss_btn = st.button('Toss a Coin')
    with result_col:
        if toss_btn:
            st.info(f"The result: {toss()}")

elif opt=="Roll a Dice":
    roll_col, result_col, dum = st.columns([1,1,5])
    with roll_col:
        roll_btn = st.button('Roll a Dice')
    with result_col:
        if roll_btn:
            st.info(f"The number: {roll()}")

else:
    min_col, max_col, pick_col = st.columns([3,3,1])
    with min_col:
        min_val = st.number_input('Enter min number:',min_value=1,step=1)
    with max_col:
        max_val = st.number_input('Enter max number:',min_value=min_val+1, step=1)
    with pick_col:
        pick_btn = st.button('Pick Number')
    if pick_btn:
        st.markdown('\n')
        st.info(f"The number: {pick_number(min_val,max_val)}")

