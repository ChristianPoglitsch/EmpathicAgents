```
The LLM lives in the real world BUT like every living being,
you only know known buildings in the area you live in,
you know more about the street you live in,
and you know the most about the house you live in.

You come to know other locations, if you have visted them.
You add buildings to your memory if you have visited them, etc.
```

> #FIXME: is quite different from the paper.
* there is no maze where events / chats are attached to tiles.
* there is no game obejcts that are activated once the person has travelled near it.



There is a need to query the LLM for what the agent will possibly know of its location.
for example, the agent might know a lot about kortrijk, but almost nothing about ieper.
This specific spatial knowledge should be made in advance and it is easier to add things to it, than to remove it (forget it)

the agent should also not know a location if it isnt in the spatial memory.

This is not present in the paper 'generative agents', they hard coded the possible locations, which made sense since it was a game.   