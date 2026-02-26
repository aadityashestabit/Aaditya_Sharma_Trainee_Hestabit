export const encodeCursor = (data) => {
  return Buffer.from(JSON.stringify(data)).toString("base64");
};

export const decodeCursor = (cursor) => {
  return JSON.parse(
    Buffer.from(cursor, "base64").toString("ascii")
  );
};