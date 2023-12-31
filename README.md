<div style="text-align: center">

<img src="assets/Logo.png" alt="TEC-Toolkit Logo" width=10% />

</div>

## CPSWatch - Cyber Physical System Monitoring Ontology
**Repository for the "CPSWatch" ontology.**

This ontology defines a vocabulary for describing cyber physical systems for monitoring purpose. It contains two main concepts: **CPSWatch#MonitoredSystem** that is a top level description of a System that is modeled and **CPSWatch#MonitoringSensor** that is a top level description of a sensor used to monitor the CPSWatch#MonitoredSystem. 

The cyber physical system can be modeled by using serveral instances of a **CPSWatch#MonitoredSystem** and combine them by using **hasSystemConnection** to model that one system has an outgoing connection to another instance or use **hasSubSystem** to model a hierarchy of the system.
There are three subclasses for the **CPSWatch#MonitoringSensor**. One for a sensor that creates numeric data with a fixed updateRate (equidistant), the **ContinuousMonitoringSensor**, another for a sensor that creates numeric data, but with an event based update behavior, the **EventMonitoringSensor** and a last one for status text the **StatusMonitoringSensor**.
These sensors can be connected to a **CPSWatch#MonitoredSystem** via **hasMonitoringSensor**. To make it possible to include knowledge about the influence of sensors on each other the ObjectProperty **hasInfluence** can be used. If more information about the type of influence is available this can be modeled by **hasPositiveCorrelation** or **hasNegativeCorrelation**. 

The connections of the **CPSWatch#MonitoredSystem** instances and the **CPSWatch#MonitoringSensor** instances can be benefitial for monitoring purpose and for diagnosis of anomalies and errors.

For identification purpose each **CPSWatch#MonitoredSystem** and **CPSWatch#MonitoringSensor** need a unique ID, moedeled by **hasID**.

The observations of the sensors are modeled using **CPSWatch#Observation** and the corresponding subclasses **NumericObservation** and **StatusObservation**. These classes use properties defined by the [sosa ontology](https://www.w3.org/TR/vocab-ssn/#intro) to make the observations reusable with more complex ssn / sosa modeled cyber physical systems.  

The minimal columns of a dataset only provide a dateTime column, a column with the ID of the **CPSWatch#MonitoringSensor** and the corresponding value in the Value column. To not mix numeric values and strings one should provide a seperate dataset for the status sensors.

## Contact
This space is administered by:  

**Bjoern Ludwig**  
*PhD Student*  
[Helmut-Schmidt-University](https://www.hsu-hh.de/en/)  
Hamburg, Germany  
<bjoern.ludwig@hsu-hh.de>  
GitHub: [B-Ludwig](https://github.com/B-Ludwig/) 
ORCID: [0009-0003-2548-8225](https://orcid.org/0009-0003-2548-8225)  

[![DOI](https://zenodo.org/badge/705643881.svg)](https://zenodo.org/doi/10.5281/zenodo.10159969)
