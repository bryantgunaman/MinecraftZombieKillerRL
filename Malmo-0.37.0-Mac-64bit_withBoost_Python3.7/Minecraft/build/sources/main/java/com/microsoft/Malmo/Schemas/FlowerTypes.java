//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2020.01.10 at 01:08:05 PM PST 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for FlowerTypes.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * <p>
 * <pre>
 * &lt;simpleType name="FlowerTypes">
 *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *     &lt;enumeration value="dandelion"/>
 *     &lt;enumeration value="poppy"/>
 *     &lt;enumeration value="blue_orchid"/>
 *     &lt;enumeration value="allium"/>
 *     &lt;enumeration value="houstonia"/>
 *     &lt;enumeration value="red_tulip"/>
 *     &lt;enumeration value="orange_tulip"/>
 *     &lt;enumeration value="white_tulip"/>
 *     &lt;enumeration value="pink_tulip"/>
 *     &lt;enumeration value="oxeye_daisy"/>
 *   &lt;/restriction>
 * &lt;/simpleType>
 * </pre>
 * 
 */
@XmlType(name = "FlowerTypes")
@XmlEnum
public enum FlowerTypes {

    @XmlEnumValue("dandelion")
    DANDELION("dandelion"),
    @XmlEnumValue("poppy")
    POPPY("poppy"),
    @XmlEnumValue("blue_orchid")
    BLUE_ORCHID("blue_orchid"),
    @XmlEnumValue("allium")
    ALLIUM("allium"),
    @XmlEnumValue("houstonia")
    HOUSTONIA("houstonia"),
    @XmlEnumValue("red_tulip")
    RED_TULIP("red_tulip"),
    @XmlEnumValue("orange_tulip")
    ORANGE_TULIP("orange_tulip"),
    @XmlEnumValue("white_tulip")
    WHITE_TULIP("white_tulip"),
    @XmlEnumValue("pink_tulip")
    PINK_TULIP("pink_tulip"),
    @XmlEnumValue("oxeye_daisy")
    OXEYE_DAISY("oxeye_daisy");
    private final String value;

    FlowerTypes(String v) {
        value = v;
    }

    public String value() {
        return value;
    }

    public static FlowerTypes fromValue(String v) {
        for (FlowerTypes c: FlowerTypes.values()) {
            if (c.value.equals(v)) {
                return c;
            }
        }
        throw new IllegalArgumentException(v);
    }

}
