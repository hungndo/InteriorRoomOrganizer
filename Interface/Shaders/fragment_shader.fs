#version 330

in vec2 outTexCoords;
in vec3 surfaceNormal;

out vec4 outColor;
uniform sampler2D samplerTexture;

void main()
{
    vec3 ambientLightIntensity = vec3(1.0f, 1.0f, 1.0f);
    vec3 sunLightIntensity = vec3(0.5f, 0.5f, 0.5f);
    vec3 sunLightDirection = normalize(vec3(-2.0f, -2.0f, 1.0f));

    vec4 textureElement = texture(samplerTexture, outTexCoords);
    vec3 lightIntensity = ambientLightIntensity + sunLightIntensity * max(dot(surfaceNormal, sunLightDirection),0.0f);
    outColor = vec4(textureElement.rbg * lightIntensity, textureElement.a);
}