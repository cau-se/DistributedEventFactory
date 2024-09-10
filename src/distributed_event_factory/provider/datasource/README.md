# Data Source

Data Sources are the heart of DEF. They are defined by 3 properties:

- `name:` Simply the name of the data source
- `groupId:` The name of the group it belongs to
- [`eventGenerator:`](../event/README.md) A method which defines which events it produces
- [`sink:`](../sink/README.md) A sik nk where it sends the generated events to

## Default sink
Instead of giving each data source its own sink a default sink can be defined which applies for all sink.

It is defined in this way:
```yaml
defaultSink:
  type: console
```

## Example Configuration
An exemplary example of a data source looks like this
```yaml
name: "GoodsDelivery"
groupId: "factory"
eventGeneration: [...]
sink: console
```