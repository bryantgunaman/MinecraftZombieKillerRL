//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2020.01.21 at 01:10:55 PM PST 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
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
 *       &lt;all>
 *         &lt;element name="ModifierList" minOccurs="0">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;restriction base="{http://ProjectMalmo.microsoft.com}CommandListModifier">
 *                 &lt;choice maxOccurs="unbounded">
 *                   &lt;element name="command" type="{http://ProjectMalmo.microsoft.com}HumanLevelCommand" maxOccurs="unbounded" minOccurs="0"/>
 *                 &lt;/choice>
 *               &lt;/restriction>
 *             &lt;/complexContent>
 *           &lt;/complexType>
 *         &lt;/element>
 *       &lt;/all>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {

})
@XmlRootElement(name = "HumanLevelCommands")
public class HumanLevelCommands {

    @XmlElement(name = "ModifierList")
    protected HumanLevelCommands.ModifierList modifierList;

    /**
     * Gets the value of the modifierList property.
     * 
     * @return
     *     possible object is
     *     {@link HumanLevelCommands.ModifierList }
     *     
     */
    public HumanLevelCommands.ModifierList getModifierList() {
        return modifierList;
    }

    /**
     * Sets the value of the modifierList property.
     * 
     * @param value
     *     allowed object is
     *     {@link HumanLevelCommands.ModifierList }
     *     
     */
    public void setModifierList(HumanLevelCommands.ModifierList value) {
        this.modifierList = value;
    }


    /**
     * <p>Java class for anonymous complex type.
     * 
     * <p>The following schema fragment specifies the expected content contained within this class.
     * 
     * <pre>
     * &lt;complexType>
     *   &lt;complexContent>
     *     &lt;restriction base="{http://ProjectMalmo.microsoft.com}CommandListModifier">
     *       &lt;choice maxOccurs="unbounded">
     *         &lt;element name="command" type="{http://ProjectMalmo.microsoft.com}HumanLevelCommand" maxOccurs="unbounded" minOccurs="0"/>
     *       &lt;/choice>
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "")
    public static class ModifierList
        extends CommandListModifier
    {


    }

}
