import streamlit
import snowflake.connector

streamlit.title('hii');
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(),CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)




import streamlit
import snowflake.connector
import pandas

streamlit.title("Zena's Amazing Athleisure Catalog")

# Connect to Snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

# Run a Snowflake query and put it all in a var called my_catalog
my_cur.execute("SELECT color_or_style FROM catalog_for_website")
my_catalog = my_cur.fetchall()

# Put the data into a dataframe
df = pandas.DataFrame(my_catalog)

# Temporarily write the dataframe to the page so I can see what I am working with
# streamlit.write(df)

# Put the first column into a list
color_list = df[0].values.tolist()

# Let's put a pick list here so they can pick the color
option = streamlit.selectbox('Pick a sweatsuit color or style:', list(color_list))

# We'll build the image caption now, since we can
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

# Use the option selected to go back and get all the info from the database
my_cur.execute(
    "SELECT direct_url, price, size_list, upsell_product_desc FROM catalog_for_website WHERE color_or_style = '" + option + "';"
)
df2 = my_cur.fetchone()

streamlit.image(df2[0], width=400, caption=product_caption)
streamlit.write('Price: ', df2[1])
streamlit.write('Sizes Available: ', df2[2])
streamlit.write(df2[3])
