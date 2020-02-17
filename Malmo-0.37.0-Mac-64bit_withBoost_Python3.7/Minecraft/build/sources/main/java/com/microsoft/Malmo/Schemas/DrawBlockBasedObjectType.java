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
import javax.xml.bind.annotation.XmlSeeAlso;
import javax.xml.bind.annotation.XmlType;


/**
 * 
 *         Base class for all block-based draw objects.
 *       
 * 
 * <p>Java class for DrawBlockBasedObjectType complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="DrawBlockBasedObjectType">
 *   &lt;complexContent>
 *     &lt;extension base="{http://ProjectMalmo.microsoft.com}DrawObjectType">
 *       &lt;attribute name="type" use="required" type="{http://ProjectMalmo.microsoft.com}BlockType" />
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
@XmlType(name = "DrawBlockBasedObjectType")
@XmlSeeAlso({
    DrawSphere.class,
    DrawBlock.class,
    DrawCuboid.class,
    DrawLine.class
})
public class DrawBlockBasedObjectType
    extends DrawObjectType
{

    @XmlAttribute(name = "type", required = true)
    protected BlockType type;
    @XmlAttribute(name = "variant")
    protected Variation variant;
    @XmlAttribute(name = "colour")
    protected Colour colour;
    @XmlAttribute(name = "face")
    protected Facing face;

    /**
     * Gets the value of the type property.
     * 
     * @return
     *     possible object is
     *     {@link BlockType }
     *     
     */
    public BlockType getType() {
        return type;
    }

    /**
     * Sets the value of the type property.
     * 
     * @param value
     *     allowed object is
     *     {@link BlockType }
     *     
     */
    public void setType(BlockType value) {
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
