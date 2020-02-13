//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2020.02.13 at 01:35:12 PM PST 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
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
 *                   &lt;element name="command" type="{http://ProjectMalmo.microsoft.com}MissionQuitCommand" maxOccurs="unbounded" minOccurs="0"/>
 *                 &lt;/choice>
 *               &lt;/restriction>
 *             &lt;/complexContent>
 *           &lt;/complexType>
 *         &lt;/element>
 *       &lt;/all>
 *       &lt;attribute name="quitDescription" type="{http://www.w3.org/2001/XMLSchema}string" default="" />
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
@XmlRootElement(name = "MissionQuitCommands")
public class MissionQuitCommands {

    @XmlElement(name = "ModifierList")
    protected MissionQuitCommands.ModifierList modifierList;
    @XmlAttribute(name = "quitDescription")
    protected String quitDescription;

    /**
     * Gets the value of the modifierList property.
     * 
     * @return
     *     possible object is
     *     {@link MissionQuitCommands.ModifierList }
     *     
     */
    public MissionQuitCommands.ModifierList getModifierList() {
        return modifierList;
    }

    /**
     * Sets the value of the modifierList property.
     * 
     * @param value
     *     allowed object is
     *     {@link MissionQuitCommands.ModifierList }
     *     
     */
    public void setModifierList(MissionQuitCommands.ModifierList value) {
        this.modifierList = value;
    }

    /**
     * Gets the value of the quitDescription property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getQuitDescription() {
        if (quitDescription == null) {
            return "";
        } else {
            return quitDescription;
        }
    }

    /**
     * Sets the value of the quitDescription property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setQuitDescription(String value) {
        this.quitDescription = value;
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
     *         &lt;element name="command" type="{http://ProjectMalmo.microsoft.com}MissionQuitCommand" maxOccurs="unbounded" minOccurs="0"/>
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
