//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2020.02.14 at 02:06:32 AM PST 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for anonymous complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;attribute name="biome" type="{http://www.w3.org/2001/XMLSchema}int" />
 *       &lt;attribute name="forceReset" type="{http://www.w3.org/2001/XMLSchema}boolean" default="false" />
 *       &lt;attribute name="destroyAfterUse" type="{http://www.w3.org/2001/XMLSchema}boolean" default="true" />
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "")
@XmlRootElement(name = "BiomeGenerator")
public class BiomeGenerator {

    @XmlAttribute(name = "biome")
    protected Integer biome;
    @XmlAttribute(name = "forceReset")
    protected Boolean forceReset;
    @XmlAttribute(name = "destroyAfterUse")
    protected Boolean destroyAfterUse;

    /**
     * Gets the value of the biome property.
     * 
     * @return
     *     possible object is
     *     {@link Integer }
     *     
     */
    public Integer getBiome() {
        return biome;
    }

    /**
     * Sets the value of the biome property.
     * 
     * @param value
     *     allowed object is
     *     {@link Integer }
     *     
     */
    public void setBiome(Integer value) {
        this.biome = value;
    }

    /**
     * Gets the value of the forceReset property.
     * 
     * @return
     *     possible object is
     *     {@link Boolean }
     *     
     */
    public boolean isForceReset() {
        if (forceReset == null) {
            return false;
        } else {
            return forceReset;
        }
    }

    /**
     * Sets the value of the forceReset property.
     * 
     * @param value
     *     allowed object is
     *     {@link Boolean }
     *     
     */
    public void setForceReset(Boolean value) {
        this.forceReset = value;
    }

    /**
     * Gets the value of the destroyAfterUse property.
     * 
     * @return
     *     possible object is
     *     {@link Boolean }
     *     
     */
    public boolean isDestroyAfterUse() {
        if (destroyAfterUse == null) {
            return true;
        } else {
            return destroyAfterUse;
        }
    }

    /**
     * Sets the value of the destroyAfterUse property.
     * 
     * @param value
     *     allowed object is
     *     {@link Boolean }
     *     
     */
    public void setDestroyAfterUse(Boolean value) {
        this.destroyAfterUse = value;
    }

}
