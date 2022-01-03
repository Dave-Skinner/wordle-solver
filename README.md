# wordle-solver
Solver for Wordle game https://www.powerlanguage.co.uk/wordle/


To solve for any specific 5 letter guess word and answer:

```
df = getWordsDF()
solveWordle(guess_word, answer, df)
```

To run trials with specific or random guess words and answers:

```
runTrials(guess_word=None, answer=None, trials=100)
```
Leaving guess_word or answer as None will randomise them for each trial.

