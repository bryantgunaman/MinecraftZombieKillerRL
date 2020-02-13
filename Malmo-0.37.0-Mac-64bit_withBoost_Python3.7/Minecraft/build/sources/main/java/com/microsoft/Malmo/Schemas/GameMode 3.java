//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2020.02.05 at 06:54:40 PM PST 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for GameMode.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * <p>
 * <pre>
 * &lt;simpleType name="GameMode">
 *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *     &lt;enumeration value="Survival"/>
 *     &lt;enumeration value="Creative"/>
 *     &lt;enumeration value="Adventure"/>
 *     &lt;enumeration value="Spectator"/>
 *   &lt;/restriction>
 * &lt;/simpleType>
 * </pre>
 * 
 */
@XmlType(name = "GameMode")
@XmlEnum
public enum GameMode {

    @XmlEnumValue("Survival")
    SURVIVAL("Survival"),
    @XmlEnumValue("Creative")
    CREATIVE("Creative"),
    @XmlEnumValue("Adventure")
    ADVENTURE("Adventure"),
    @XmlEnumValue("Spectator")
    SPECTATOR("Spectator");
    private final String value;

    GameMode(String v) {
        value = v;
    }

    public String value() {
        return value;
    }

    public static GameMode fromValue(String v) {
        for (GameMode c: GameMode.values()) {
            if (c.value.equals(v)) {
                return c;
            }
        }
        throw new IllegalArgumentException(v);
    }

}
