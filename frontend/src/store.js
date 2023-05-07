import { configureStore } from "@reduxjs/toolkit";
import reducer from "./app/slice";

const store = configureStore({
  reducer: {
    app: reducer,
  },
});

export default store;
