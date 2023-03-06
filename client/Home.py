import streamlit as st
import time
import asyncio
import random
import json
from threading import Thread
from kafka import KafkaConsumer
from streamlit.runtime.scriptrunner import add_script_run_ctx


def kafka_thread():
    consumer = KafkaConsumer(
        'messages',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )
    for message in consumer:
        key = message.key.decode('utf8').replace("'", '"')
        value = json.loads(message.value.decode('utf8').replace("'", '"'))
        st.session_state.data.append(value)


async def update_message():
    data = st.session_state.data
    for index, item in list(reversed(list(enumerate(data))))[:10]:
        col0, col1, col2, col3, col4 = st.columns([1, 10, 2, 2, 2])
        col0.markdown(
            f"""<p style="font-size:25px">{index + 1}</>""", unsafe_allow_html=True)
        col1.markdown(
            f"""<p style="font-size:25px">{item['content']}</>""", unsafe_allow_html=True)
        col2.write(item['from_user'])

        if item['label'] != 2:
            col3.markdown(
                f"""<p style="color:{"green" if item['label']==0 else "red"};font-size:25px">{"Reliable" if item['label']==0 else "Unreliable"}</p>""", unsafe_allow_html=True)
        else:
            col3.write('Waiting')

        col4.button('Train', key=time.time(),
                    on_click=lambda index: show_noti(index), args=[index])


async def update_metrics():
    await asyncio.sleep(random.randint(1, 3))
    old = st.session_state.accuracy
    st.session_state.accuracy += random.random() * random.choice([1, -1])
    st.metric(label="Accuracy",
              value=f"{round(st.session_state.accuracy, 2)} %", delta=f"{round(st.session_state.accuracy - old, 2)} %")


def show_noti(index):
    st.info(f"Đã train lại post số {index + 1}", icon="✅")


# init session_state
if 'data' not in st.session_state:
    st.session_state.data = []

if 'accuracy' not in st.session_state:
    st.session_state.accuracy = 0

st.set_page_config(layout="wide")


async def main():
    with st.empty():
        while True:
            tab1, tab2 = st.tabs(["Bài đăng mới", "Trạng thái mô hình"])
            with tab1:
                await(asyncio.gather(update_message()))
            with tab2:
                await(asyncio.gather(update_metrics()))


if __name__ == '__main__':

    # update new post as background task
    t = Thread(target=kafka_thread, daemon=True)
    add_script_run_ctx(t)
    t.start()

    # start app loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
