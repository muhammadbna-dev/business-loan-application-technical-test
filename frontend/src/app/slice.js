import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import URLS from "./constants/urls";
import callApi from "../utils/apiUtils";

const initialState = {
  testApiResult: "-",
};

export const testApi = createAsyncThunk("app/testApi", async () => {
  const data = await callApi(URLS.TEST_API(), "GET");
  return data;
});

export const slice = createSlice({
  name: "app",
  initialState,
  reducers: {
    foo: (state, action) => {},
  },
  extraReducers: (builder) => {
    builder.addCase(testApi.fulfilled, (state, action) => {
      state.testApiResult = action.payload;
    });
    builder.addCase(testApi.rejected, (state, action) => {
      console.error(action.error.message);
    });
  },
});

export const { foo } = slice.actions;

export default slice.reducer;
