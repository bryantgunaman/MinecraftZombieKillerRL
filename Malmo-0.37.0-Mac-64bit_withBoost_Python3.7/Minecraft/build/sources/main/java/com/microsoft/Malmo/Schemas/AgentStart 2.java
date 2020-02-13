//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2020.02.04 at 04:47:25 PM PST 
//


package com.microsoft.Malmo.Schemas;

import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.JAXBElement;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlElementRef;
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
 *         &lt;element name="Placement" type="{http://ProjectMalmo.microsoft.com}PosAndDirection" minOccurs="0"/>
 *         &lt;element name="Inventory" minOccurs="0">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                 &lt;choice maxOccurs="unbounded" minOccurs="0">
 *                   &lt;element ref="{http://ProjectMalmo.microsoft.com}InventoryObject"/>
 *                 &lt;/choice>
 *               &lt;/restriction>
 *             &lt;/complexContent>
 *           &lt;/complexType>
 *         &lt;/element>
 *         &lt;element name="EnderBoxInventory" minOccurs="0">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                 &lt;choice maxOccurs="unbounded" minOccurs="0">
 *                   &lt;element ref="{http://ProjectMalmo.microsoft.com}InventoryObject"/>
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
@XmlRootElement(name = "AgentStart")
public class AgentStart {

    @XmlElement(name = "Placement")
    protected PosAndDirection placement;
    @XmlElement(name = "Inventory")
    protected AgentStart.Inventory inventory;
    @XmlElement(name = "EnderBoxInventory")
    protected AgentStart.EnderBoxInventory enderBoxInventory;

    /**
     * Gets the value of the placement property.
     * 
     * @return
     *     possible object is
     *     {@link PosAndDirection }
     *     
     */
    public PosAndDirection getPlacement() {
        return placement;
    }

    /**
     * Sets the value of the placement property.
     * 
     * @param value
     *     allowed object is
     *     {@link PosAndDirection }
     *     
     */
    public void setPlacement(PosAndDirection value) {
        this.placement = value;
    }

    /**
     * Gets the value of the inventory property.
     * 
     * @return
     *     possible object is
     *     {@link AgentStart.Inventory }
     *     
     */
    public AgentStart.Inventory getInventory() {
        return inventory;
    }

    /**
     * Sets the value of the inventory property.
     * 
     * @param value
     *     allowed object is
     *     {@link AgentStart.Inventory }
     *     
     */
    public void setInventory(AgentStart.Inventory value) {
        this.inventory = value;
    }

    /**
     * Gets the value of the enderBoxInventory property.
     * 
     * @return
     *     possible object is
     *     {@link AgentStart.EnderBoxInventory }
     *     
     */
    public AgentStart.EnderBoxInventory getEnderBoxInventory() {
        return enderBoxInventory;
    }

    /**
     * Sets the value of the enderBoxInventory property.
     * 
     * @param value
     *     allowed object is
     *     {@link AgentStart.EnderBoxInventory }
     *     
     */
    public void setEnderBoxInventory(AgentStart.EnderBoxInventory value) {
        this.enderBoxInventory = value;
    }


    /**
     * <p>Java class for anonymous complex type.
     * 
     * <p>The following schema fragment specifies the expected content contained within this class.
     * 
     * <pre>
     * &lt;complexType>
     *   &lt;complexContent>
     *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *       &lt;choice maxOccurs="unbounded" minOccurs="0">
     *         &lt;element ref="{http://ProjectMalmo.microsoft.com}InventoryObject"/>
     *       &lt;/choice>
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "inventoryObject"
    })
    public static class EnderBoxInventory {

        @XmlElementRef(name = "InventoryObject", namespace = "http://ProjectMalmo.microsoft.com", type = JAXBElement.class, required = false)
        protected List<JAXBElement<? extends InventoryObjectType>> inventoryObject;

        /**
         * Gets the value of the inventoryObject property.
         * 
         * <p>
         * This accessor method returns a reference to the live list,
         * not a snapshot. Therefore any modification you make to the
         * returned list will be present inside the JAXB object.
         * This is why there is not a <CODE>set</CODE> method for the inventoryObject property.
         * 
         * <p>
         * For example, to add a new item, do as follows:
         * <pre>
         *    getInventoryObject().add(newItem);
         * </pre>
         * 
         * 
         * <p>
         * Objects of the following type(s) are allowed in the list
         * {@link JAXBElement }{@code <}{@link InventoryObjectType }{@code >}
         * {@link JAXBElement }{@code <}{@link InventoryItem }{@code >}
         * {@link JAXBElement }{@code <}{@link InventoryBlock }{@code >}
         * 
         * 
         */
        public List<JAXBElement<? extends InventoryObjectType>> getInventoryObject() {
            if (inventoryObject == null) {
                inventoryObject = new ArrayList<JAXBElement<? extends InventoryObjectType>>();
            }
            return this.inventoryObject;
        }

    }


    /**
     * <p>Java class for anonymous complex type.
     * 
     * <p>The following schema fragment specifies the expected content contained within this class.
     * 
     * <pre>
     * &lt;complexType>
     *   &lt;complexContent>
     *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
     *       &lt;choice maxOccurs="unbounded" minOccurs="0">
     *         &lt;element ref="{http://ProjectMalmo.microsoft.com}InventoryObject"/>
     *       &lt;/choice>
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "inventoryObject"
    })
    public static class Inventory {

        @XmlElementRef(name = "InventoryObject", namespace = "http://ProjectMalmo.microsoft.com", type = JAXBElement.class, required = false)
        protected List<JAXBElement<? extends InventoryObjectType>> inventoryObject;

        /**
         * Gets the value of the inventoryObject property.
         * 
         * <p>
         * This accessor method returns a reference to the live list,
         * not a snapshot. Therefore any modification you make to the
         * returned list will be present inside the JAXB object.
         * This is why there is not a <CODE>set</CODE> method for the inventoryObject property.
         * 
         * <p>
         * For example, to add a new item, do as follows:
         * <pre>
         *    getInventoryObject().add(newItem);
         * </pre>
         * 
         * 
         * <p>
         * Objects of the following type(s) are allowed in the list
         * {@link JAXBElement }{@code <}{@link InventoryObjectType }{@code >}
         * {@link JAXBElement }{@code <}{@link InventoryItem }{@code >}
         * {@link JAXBElement }{@code <}{@link InventoryBlock }{@code >}
         * 
         * 
         */
        public List<JAXBElement<? extends InventoryObjectType>> getInventoryObject() {
            if (inventoryObject == null) {
                inventoryObject = new ArrayList<JAXBElement<? extends InventoryObjectType>>();
            }
            return this.inventoryObject;
        }

    }

}
