#version 330

in layout(location = 0) vec3 position;
in layout(location = 1) vec2 inTexCoords;
in layout(location = 2) vec3 normals;

uniform mat4 ModelViewProjectionMatrix;
uniform mat4 transformation;

out vec2 outTexCoords;
out vec3 surfaceNormal;

void main()
{
    surfaceNormal = (transformation * vec4(normals, 0.0f)).xyz;
    gl_Position = ModelViewProjectionMatrix * vec4(position, 1.0f);
    outTexCoords = inTexCoords;
}