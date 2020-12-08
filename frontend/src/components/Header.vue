<template>
    <v-app-bar
      app
      fixed
      flat
      elevation="3"
      color="blue">
      <h1 style="color:white">
      Proyecto 3 - Face Recognition
      </h1>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-sm-and-down">
        <v-tooltip left color="black" >
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on"  @click="go_to()">
              <v-icon large>
                mdi-github-circle
              </v-icon>     
            </v-btn>
          </template>
          <span class="white--text subheading font-weight-medium" style="color:#000000">Ver repositorio</span>
        </v-tooltip>
      </v-toolbar-items>   
    </v-app-bar>
</template>

<script>
export default {
    name: 'Header',
    methods: {
      go_to(){
         window.open("https://github.com/JuanGA12/BD2PR3", "_blank");    
      }
    }
}
</script>

<style>

</style>