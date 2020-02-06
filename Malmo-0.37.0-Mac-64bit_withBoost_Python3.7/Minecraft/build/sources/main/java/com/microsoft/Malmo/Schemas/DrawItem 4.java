//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2020.02.05 at 06:54:40 PM PST 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlType;


/**
 * 
 *         Specify an item by location and type.
 *       
 * 
 * <p>Java class for DrawItem complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="DrawItem">
 *   &lt;complexContent>
 *     &lt;extension base="{http://ProjectMalmo.microsoft.com}DrawObjectType">
 *       &lt;attribute name="x" use="required" type="{http://www.w3.org/2001/XMLSchema}int" />
 *       &lt;attribute name="y" use="required" type="{http://www.w3.org/2001/XMLSchema}int" />
 *       &lt;attribute name="z" use="required" type="{http://www.w3.org/2001/XMLSchema}int" />
 *       &lt;attribute name="type" use="required" type="{http://ProjectMalmo.microsoft.com}BlockOrItem" />
 *       &lt;attribute name="variant" type="{http://ProjectMalmo.microsoft.com}Variation" />
 *       &lt;attribute name="colour" type="{http://ProjectMalmo.microsoft.com}Colour" />
 *       &lt;attribute name="face" type="{http://ProjectMalmo.microsoft.com}Facing" />
 *     &lt;/extension>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "DrawItem")
public class DrawItem
    extends DrawObjectType
{

    @XmlAttribute(name = "x", required = true)
    protected int x;
    @XmlAttribute(name = "y", required = true)
    protected int y;
    @XmlAttribute(name = "z", required = true)
    protected int z;
    @XmlAttribute(name = "type", required = true)
    protected String type;
    @XmlAttribute(name = "variant")
    protected Variation variant;
    @XmlAttribute(name = "colour")
    protected Colour colour;
    @XmlAttribute(name = "face")
    protected Facing face;

    /**
     * Gets the value of the x property.
     * 
     */
    public int getX() {
        return x;
    }

    /**
     * Sets the value of the x property.
     * 
     */
    public void setX(int value) {
        this.x = value;
    }

    /**
     * Gets the value of the y property.
     * 
     */
    public int getY() {
        return y;
    }

    /**
     * Sets the value of the y property.
     * 
     */
    public void setY(int value) {
        this.y = value;
    }

    /**
     * Gets the value of the z property.
     * 
     */
    public int getZ() {
        return z;
    }

    /**
     * Sets the value of the z property.
     * 
     */
    public void setZ(int value) {
        this.z = value;
    }

    /**
     * Gets the value of the type property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getType() {
        return type;
    }

    /**
     * Sets the value of the type property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setType(String value) {
        this.type = value;
    }

    /**
     * Gets the value of the variant property.
     * 
     * @return
     *     possible object is
     *     {@link Variation }
     *     
     */
    public Variation getVariant() {
        return variant;
    }

    /**
     * Sets the value of the variant property.
     * 
     * @param value
     *     allowed object is
     *     {@link Variation }
     *     
     */
    public void setVariant(Variation value) {
        this.variant = value;
    }

    /**
     * Gets the value of the colour property.
     * 
     * @return
     *     possible object is
     *     {@link Colour }
     *     
     */
    public Colour getColour() {
        return colour;
    }

    /**
     * Sets the value of the colour property.
     * 
     * @param value
     *     allowed object is
     *     {@link Colour }
     *     
     */
    public void setColour(Colour value) {
        this.colour = value;
    }

    /**
     * Gets the value of the face property.
     * 
     * @return
     *     possible object is
     *     {@link Facing }
     *     
     */
    public Facing getFace() {
        return face;
    }

    /**
     * Sets the value of the face property.
     * 
     * @param value
     *     allowed object is
     *     {@link Facing }
     *     
     */
    public void setFace(Facing value) {
        this.face = value;
    }

}
