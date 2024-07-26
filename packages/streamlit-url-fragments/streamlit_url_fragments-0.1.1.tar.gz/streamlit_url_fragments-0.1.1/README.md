# Streamlit URL fragment

A fork of  [ktosiek/streamlit-url-fragment](https://github.com/ktosiek/streamlit-url-fragment)
that adds the ability to get the hash as a dictionary if it is in the correct format.

Get the URL fragment (the part of URL after #) in your Streamlit script:

```python
import streamlit as st
from streamlit_url_fragments import get_fragments

current_value = get_fragments()
st.write(f"Current value: {get_fragments()}")
```

Warning: the first value you'll get will be a `None` - that means the component is still loading.
You can wait for the correct value with `if current_value is None: st.stop()`.

This fork adds the ability to get the hash as a dictionary if it is in the correct format.
Please make sure to test the type returned by the function before using it.

```python
import streamlit as st
from streamlit_url_fragments import get_fragments

current_value = get_fragments()

if isinstance(current_value, dict):
    st.write("The function returned a dictionary.")
elif isinstance(current_value, str):
    st.write("The function returned a string.")
else:
    st.write(f"The function returned an unexpected type: {type(current_value)}")

st.write(f"Current value: {current_value}")
```