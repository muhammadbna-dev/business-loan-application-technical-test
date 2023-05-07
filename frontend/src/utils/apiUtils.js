const callApi = async (url, method, body = {}) => {
  const requestObj = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };
  if (!["GET", "HEAD"].includes(method)) {
    requestObj["body"] = JSON.stringify(body);
  }

  const response = await fetch(url, requestObj);
  const responseJson = await response.json();
  const { success = False, data = {}, message = "-" } = responseJson;
  if (!!success) {
    return data;
  } else {
    throw new Error(`Error calling API. URL ${url}. Error message: ${message}`);
  }
};

export default callApi;
