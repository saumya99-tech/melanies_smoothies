# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie
    """
)

name_on_order=st.text_input('Name of Smoothie:')
st.write('The name of your smoothie will be',name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()

# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingrdients:', my_dataframe,max_selections=5
)

if(ingredients_list):
    
    ingredients_string=''
    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit +' '
    #st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_On_ORDER)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
    #st.write(my_insert_stmt)
    
    time_to_insert= st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")

#New section to display smoothiefroot nutrition information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
    
