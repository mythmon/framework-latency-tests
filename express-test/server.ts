import express from "express";

const PORT = process.env.PORT ?? 9002;
const app = express();

let counters: {[color: string]: number} = {};

app.get("/:color", async (req, res) => {
  await sleep(10);
  let {color} = req.params;
  if (!Object.prototype.hasOwnProperty.call(counters, color)) {
    counters[color] = 0;
  }
  counters[color] += 1;
  res.json({[color]: counters[color]})
});

/**
 * @param {number} time
 * @returns {Promise<void>}
 */
function sleep(time: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, time);
  });
}

app.listen(PORT);
