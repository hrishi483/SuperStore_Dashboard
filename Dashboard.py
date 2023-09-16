import streamlit as st
import plotly.express as px
import pandas as pd
import os 
import warnings 
import plotly.figure_factory as ff
warnings.filterwarnings('ignore')


st.set_page_config(page_title="Superstore",page_icon=":bar_chart:",layout="wide")
st.title(":bar_chart: Sample Superstore EDA")

st.markdown('<style> div.block-container{padding-top: 1reem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a File",type=(["xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(filename)
# else:
#     # os.chdir(r"D:\AI Adventures\Streamlit\Sales_Dashboard")
    
#     url = "Sample.xls"
#     df = pd.read_excel(url)
    col1,col2 = st.columns((2))
    df['Order Date'] = pd.to_datetime(df["Order Date"])

    startDate = pd.to_datetime(df["Order Date"]).min()
    endDate = pd.to_datetime(df["Order Date"]).max()

    with col1:
        date1 = pd.to_datetime(st.date_input("Start Date",startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input("End Date",endDate))

    # Filter date based on input date
    df = df[(df["Order Date"]>date1)&(df["Order Date"]<date2)].copy()

    # Sidefbar to add filters
    st.sidebar.header("Choose your Filter:")
    region = st.sidebar.multiselect("Pick your Region",df["Region"].unique())
    if not region:
        df2 = df.copy()
    else:
        df2 = df[df["Region"].isin(region)]

    # Create for State:
    state = st.sidebar.multiselect("State",df2["State"].unique())
    if not state:
        df3 = df2.copy()
    else:
        df3 = df2[df2["State"].isin(state)]

    city = st.sidebar.multiselect("City",df3["City"].unique())
    if not state:
        df4 = df3.copy()
    else:
        df4 = df3[df3["State"].isin(state)]

    # Filter data based on Region , State and City
    if not region and not state and not city:
        filter_df = df
    elif not state and not city:
        filter_df = df[df["Region"].isin(region)]
    elif not region and not city:
        filter_df = df[df["State"].isin(state)]
    elif state and city:
        filter_df = df3[df["State"].isin(state) & df["City"].isin(city)]
    elif region and city:
        filter_df = df3[df["Region"].isin(region) & df["City"].isin(city)]
    elif region and state:
        filter_df = df3[df["Region"].isin(region) & df["State"].isin(state)]
    elif city:
        filter_df = df3[df["City"].isin(city)]
    else:
        filter_df = df3[df["Region"].isin(region)]

    category_df = filter_df.groupby(by = ["Category"], as_index = False)['Sales'].sum()
    # st.write(filter_df.head(5))


    with col1:
        st.subheader("Category Wise Sales")
        fig = px.bar(category_df,x="Category",y="Sales",
                    template="seaborn")
        st.plotly_chart(fig,use_container_width=True,height=200)

    with col2:
        st.subheader("Region Wise Sales")
        fig = px.pie(filter_df,values="Sales",names="Region",hole=0.5)
        fig.update_traces(text = filter_df["Region"])
        st.plotly_chart(fig,use_container_width=True)

    cl1,cl2 = st.columns(2,gap = "large")
    with cl1:
        with st.expander("Category Expander"):
            st.write(category_df)
            csv = category_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download Data",data=csv,file_name="Category.csv",
                                help="Click Download button to download as csv file")
    with cl2:
        with st.expander("Region Expander"):
            st.write(category_df)
            region_df = filter_df.groupby(by="Region",as_index=False)['Sales'].sum()
            csv=region_df.to_csv(index=False).encode('utf')
            st.download_button(label="Download Data",data=csv,file_name="Region.csv",
                                help="Click Download button to download as csv file")


    st.subheader("Time Series Analysis")
    filter_df["month_year"] = filter_df['Order Date'].dt.to_period("M")
    linechart = pd.DataFrame(filter_df.groupby(filter_df['month_year'].dt.strftime("%Y: %b"))["Sales"].sum().reset_index())

    fig2=px.line(linechart,x="month_year",y="Sales",labels={"Sales":"Amount"},height=500,width=1000
                ,template="gridon")
    fig2.update_layout({
        'plot_bgcolor': '#0C043F',
        # 'paper_bgcolor': '#00ffff',
    })
    st.plotly_chart(fig2,use_container_width=True)

    with st.expander("Expand Time Series Data"):
        st.write(linechart.T)
        st.download_button(label="Download Time Series Data",data="csv",file_name="Time-Series.csv",
                        help="Click Download button to download file as csv")

    chart1,chart2 = st.columns((2)) 
    with chart1:
        st.subheader("Segment wise Sales")
        fig3 = px.pie(filter_df,values="Sales",names="Segment",template="plotly_dark")
        fig3.update_traces(text = filter_df['Segment'],textposition = "inside")
        st.plotly_chart(fig3,use_container_width=True)

    with chart2:
        st.subheader("Category Wise Analysis")
        fig4 = px.pie(filter_df,values="Sales",names="Category",template="gridon")
        fig4.update_traces(text = filter_df['Category'],textposition = "inside")
        st.plotly_chart(fig4,use_container_width=True)

    st.subheader(":point_right: Month wise sub-Category Sales Summary")
    with st.expander("Summary_Table"):
        df_sample = df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
        fig5 = ff.create_table(df_sample, colorscale='viridis')
        st.plotly_chart(fig5,use_container_width=True)

        st.markdown("Month wise sub-Category Table")
        filter_df['month'] = filter_df['Order Date'].dt.month_name()
        sub_category_year = pd.pivot_table(data=filter_df,values="Sales",index=['Sub-Category'],columns="month")
        st.write(sub_category_year)

    # Create the scatter Plot
    data1 = px.scatter(filter_df,x="Sales",y="Profit",size="Quantity")
    data1["layout"].update(
                        title="Relationship between Sales and Profit using Scatter plot",
                        title_font_size=29,
                        yaxis = dict(title="Profit",titlefont={'size':19})
                        )
    data1.update_layout({
        'plot_bgcolor': '#006699',
        # 'paper_bgcolor': '#00ffff',
    })
    st.plotly_chart(data1,use_container_width=True)
else:
    st.write("Enter the csv file")
