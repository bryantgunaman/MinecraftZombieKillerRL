//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2020.02.04 at 04:47:25 PM PST 
//


package com.microsoft.Malmo.Schemas;

import java.math.BigDecimal;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.bind.annotation.adapters.CollapsedStringAdapter;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;


/**
 * 
 *         Used by {{{ObservationFromNearbyEntities}}}. Defines the range within which entities will be returned. Eg a range of 10,1,10 will return all entities within +/-10 blocks of the agent in the x and z axes, and within +/-1 block vertically.
 *         
 *         {{{update_frequency}}} is measured in Minecraft world ticks, and allows the user to specify how often they would like to receive each observation. A value of 20, under normal Minecraft running conditions, for example, would return the entity list once per second.
 *       
 * 
 * <p>Java class for RangeDefinition complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="RangeDefinition">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="name" use="required" type="{http://www.w3.org/2001/XMLSchema}Name" />
 *       &lt;attribute name="xrange" use="required" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="yrange" use="required" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="zrange" use="required" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *       &lt;attribute name="update_frequency" type="{http://www.w3.org/2001/XMLSchema}int" default="1" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "RangeDefinition")
public class RangeDefinition {

    @XmlAttribute(name = "name", required = true)
    @XmlJavaTypeAdapter(CollapsedStringAdapter.class)
    @XmlSchemaType(name = "Name")
    protected String name;
    @XmlAttribute(name = "xrange", required = true)
    protected BigDecimal xrange;
    @XmlAttribute(name = "yrange", required = true)
    protected BigDecimal yrange;
    @XmlAttribute(name = "zrange", required = true)
    protected BigDecimal zrange;
    @XmlAttribute(name = "update_frequency")
    protected Integer updateFrequency;

    /**
     * Gets the value of the name property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getName() {
        return name;
    }

    /**
     * Sets the value of the name property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setName(String value) {
        this.name = value;
    }

    /**
     * Gets the value of the xrange property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getXrange() {
        return xrange;
    }

    /**
     * Sets the value of the xrange property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setXrange(BigDecimal value) {
        this.xrange = value;
    }

    /**
     * Gets the value of the yrange property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getYrange() {
        return yrange;
    }

    /**
     * Sets the value of the yrange property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setYrange(BigDecimal value) {
        this.yrange = value;
    }

    /**
     * Gets the value of the zrange property.
     * 
     * @return
     *     possible object is
     *     {@link BigDecimal }
     *     
     */
    public BigDecimal getZrange() {
        return zrange;
    }

    /**
     * Sets the value of the zrange property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigDecimal }
     *     
     */
    public void setZrange(BigDecimal value) {
        this.zrange = value;
    }

    /**
     * Gets the value of the updateFrequency property.
     * 
     * @return
     *     possible object is
     *     {@link Integer }
     *     
     */
    public int getUpdateFrequency() {
        if (updateFrequency == null) {
            return  1;
        } else {
            return updateFrequency;
        }
    }

    /**
     * Sets the value of the updateFrequency property.
     * 
     * @param value
     *     allowed object is
     *     {@link Integer }
     *     
     */
    public void setUpdateFrequency(Integer value) {
        this.updateFrequency = value;
    }

}
