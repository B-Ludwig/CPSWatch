# Competency Questions

The list of CPSWatch competency questions.

## SPARQL queries used for implementing the CQs

### CQ1: Which systems are part of the CPS?

```sparql
PREFIX cpswatch: <https://w3id.org/CPSWatch#>

SELECT ?monitoredSystem
WHERE {
	?monitoredSystem a cpswatch:MonitoredSystem
}
```

#### Answer

| <http://example.org/FuelSystem> |
| <http://example.org/Pump> |
| <http://example.org/Tank> |
| <http://example.org/Engine> |

### CQ2: Which systems does Engine depend on?

```sparq2
PREFIX cpswatch: <https://w3id.org/CPSWatch#>

SELECT ?dependentSystem
WHERE {
  ?dependentSystem cpswatch:hasSystemConnection <http://example.org/Engine> .
}
```

#### Answer

| <http://example.org/FuelSystem> |

### CQ3: What sensors does the FuelSystem have?

```sparq3
PREFIX cpswatch: <https://w3id.org/CPSWatch#>

SELECT ?sensor
WHERE {
  <http://example.org/FuelSystem> cpswatch:hasMonitoringSensor ?sensor .
}
}
```

#### Answer

| <http://example.org/FS_Status> |

### CQ4: What type of sensor is sensor with ID 22001?

```sparq4
PREFIX cpswatch: <https://w3id.org/CPSWatch#>

SELECT ?sensorType
WHERE {
  ?sensor cpswatch:hasID "22001"^^xsd:nonNegativeInteger .
  ?sensor rdf:type ?sensorType .
}
```

#### Answer

|cpswatch:NumericMonitoringSensor|
|cpswatch:MonitoringSensor|
|cpswatch:EventMonitoringSensor|
|owl:Thing|

### CQ5: Which properties are observed by system XY?

```sparq5
PREFIX cpswatch: <https://w3id.org/CPSWatch#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>

SELECT ?observedProperty
WHERE {
  <http://example.org/FS_Pump_Flow> sosa:observes ?observedProperty .
}
```

#### Answer

| <http://example.org/Fuel_Flow> |

### CQ6: What is the samplerate of sensor FS_Pump_Flow? (only with continuous example)

```sparq6
PREFIX cpswatch: <https://w3id.org/CPSWatch#>

SELECT ?deviationThreshold
WHERE {
  <http://example.org/FS_Pump_Flow> cpswatch:hasSampleRate ?deviationThreshold .
}
```

#### Answer

|10.0|

### CQ7: What is the deviation threshold of sensor FS_Pump_Flow? (only with event example)

```sparq7
PREFIX cpswatch: <https://w3id.org/CPSWatch#>

SELECT ?deviationThreshold
WHERE {
  <http://example.org/FS_Pump_Flow> cpswatch:hasDeviationThreshold ?deviationThreshold .
}
```

#### Answer

|5.0|

### CQ8: Which sensor made the observation http://example.org/Observation_0?

```sparq8
PREFIX cpswatch: <https://w3id.org/CPSWatch#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>

SELECT ?sensor
WHERE {
  <http://example.org/Observation_0> sosa:madeBySensor ?sensor .
}
```

#### Answer

| <http://example.org/FS_Pump_Flow> |

### CQ9: What sensors influence sensor XZ?

```sparq9
PREFIX cpswatch: <https://w3id.org/CPSWatch#>

SELECT ?dependentSensor
WHERE {
  ?dependentSensor cpswatch:hasInfluence <http://example.org/Engine_Flow> .
}
```

#### Answer

| http://example.org/FS_Pump_Flow |


### CQ10: What status states are possible for sensor ?

```sparq10
PREFIX cpswatch: <https://w3id.org/CPSWatch#>

SELECT ?states
WHERE {
  <http://example.org/FS_Status> cpswatch:hasStates ?states .
}
```

#### Answer

| cpswatch:ShuttingDown |
| cpswatch:Off |
| cpswatch:Starting |
| cpswatch:On |

