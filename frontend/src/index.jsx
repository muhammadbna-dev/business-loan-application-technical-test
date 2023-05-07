import React from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";

import store from "./store";
import { App } from "./app";

const app = document.getElementById("app");
const root = createRoot(app);

root.render(
  <Provider store={store}>
    <App />
  </Provider>
);
