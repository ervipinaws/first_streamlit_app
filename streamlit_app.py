import streamlit
import pandas

streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")


my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])

# Display the table on the page.
#streamlit.dataframe(my_fruit_list)

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


#New section to display fruityvice api response
import requests
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#it only displays text --> streamlit.text(fruityvice_response.json()) 

# format json output as a table 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display dataframe/table
streamlit.dataframe(fruityvice_normalized)

########################################################################################33
import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
#my_data_row = my_cur.fetchone() #it fetches only first row
my_data_rows = my_cur.fetchall() 
#streamlit.text("Hello from Snowflake:")
#streamlit.text("The fruit load list contains:")
streamlit.header("The fruit load list contains:")
#streamlit.text(my_data_row)
#streamlit.dataframe(my_data_row)
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add')
streamlit.write('The user entered ', add_my_fruit)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.fruit_load_list values ('" + add_my_fruit + "')")
