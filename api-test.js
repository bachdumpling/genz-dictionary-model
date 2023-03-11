const { Configuration, OpenAIApi } = require("openai");
const key = "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";
const configuration = new Configuration({
  apiKey: key,
});

const openai = new OpenAIApi(configuration);

openai
  .createCompletion({
    model: "gpt-3.5-turbo",
    message: [{ role: "user", content: "Hello!" }],
    // max_tokens: 200,
    // temperature: 0,
  })
  .then((response) => {
    const answer = response.data.choices[0].message.content;
    console.log(answer);
  });
