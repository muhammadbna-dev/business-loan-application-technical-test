import React from "react";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";

import { testApi } from "./slice";

export const App = () => {
  const testApiResult = useSelector((state) => state.app.testApiResult);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(testApi());
  }, []);

  return (
    <div>
      Hello from React
      <p>Test API result: {testApiResult}</p>
    </div>
  );
};

export default App;
