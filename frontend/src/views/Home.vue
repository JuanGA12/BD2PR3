<template>
  <v-container>
    <v-row justify="center">
      <v-col class="mb-3 mt-3" cols="7" justify="center" align="center">
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-card elevation="6" color="blue lighten-3" style=" border-radius: 10px;">
            <v-container>
              <v-col cols="12" justify="center" align="center">
                <v-hover v-slot:default="{ hover }">
                  <v-card 
                  :elevation="hover ? 24 : 4"
                  color=#FAFAFA style=" border-radius: 15px;">
                    <v-container>
                      <v-file-input v-model="image" :rules="fileRules" :disabled="dis"
                        placeholder="Subir tu imagen"
                        label="Imagen"
                        prepend-icon="mdi-camera"
                        outlined
                        show-size
                        class="pa-3"
                        accept="image/*"
                        required>
                          <template v-slot:selection="{ text }">
                            <v-chip
                              small
                              label
                              color="primary"
                            >
                              {{ text }}  
                            </v-chip>
                          </template>
                      </v-file-input>
                    </v-container>
                  </v-card>
                </v-hover>
              </v-col>
              <v-col cols="5" justify="center" align="center">
                <v-hover v-slot:default="{ hover }">
                  <v-card 
                  :elevation="hover ? 24 : 4"
                  color=#FAFAFA style=" border-radius: 15px;">
                    <v-container>
                      <v-select v-model="Algoritmo" :items="Algoritmos" :rules="[v => !!v || 'Algoritmo es requerido']"
                        label="Algoritmo" required  placeholder="Escoge un algoritmo"
                        :disabled="dis"
                        >
                      </v-select>
                    </v-container>
                  </v-card>
                </v-hover>
              </v-col>
            <v-col cols="4" v-if="Algoritmo == 'KNN-Sequential' || Algoritmo == 'KNN-Rtree'">
              <v-hover v-slot:default="{ hover }">
                <v-card 
                :elevation="hover ? 24 : 4"
                color=#FAFAFA style=" border-radius: 15px;">
                  <v-container>
                    <v-text-field :disabled="dis"
                      v-model="K"
                        :rules="[v => !!v || 'Valor de K requerido']"
                        label="Ingrese el valor de K"
                        required
                        placeholder="K"
                      >
                    </v-text-field>
                  </v-container>
                </v-card>
              </v-hover>
            </v-col>
            <v-col cols="4" v-if="Algoritmo == 'Range Search-RTree'">
              <v-hover v-slot:default="{ hover }">
                <v-card 
                :elevation="hover ? 24 : 4"
                color=#FAFAFA style=" border-radius: 15px;">
                  <v-container>
                    <v-text-field :disabled="dis"
                      v-model="R"
                        :rules="[v => !!v || 'Valor del radio requerido']"
                        label="Ingrese el valor del radio"
                        required
                        placeholder="R"
                      >
                    </v-text-field>
                  </v-container>
                </v-card>
              </v-hover>
            </v-col>
            <v-col cols="12" v-if="R > 0 || K > 0">
              <v-hover v-slot:default="{ hover }">
                <v-card 
                :elevation="hover ? 24 : 4"
                color=#FAFAFA style=" border-radius: 15px;">
                  <v-container>
                      <v-card-title class="justify-center">
                        <span class="body-2">Cantidad de datos a utilizar</span>
                      </v-card-title>
                      <v-slider 
                        :disabled="dis"
                        v-model="P"
                        :color="color"
                        :tick-labels="Valores_p"
                        track-color="blue lighten-3"
                        :max="7"
                        step="1"
                        ticks="always"
                        tick-size="8s"
                      >
                        <template v-slot:prepend>
                          <v-icon color="red" @click="decrement">
                            mdi-minus
                          </v-icon>
                        </template>
                        <template v-slot:append>
                          <v-icon color="green" @click="increment">
                            mdi-plus
                          </v-icon>
                        </template>
                      </v-slider>
                  </v-container>
                </v-card>
              </v-hover>
            </v-col>
            <v-btn v-if="K > 0 || R > 0 " color="success" class="mr-4 mt-3 mb-3" :disabled="!valid" @click="cargar" justify="center" align="center">
              Realizar {{this.Algoritmo}}
            </v-btn>
            <v-btn v-if="K > 0  || R > 0 " color="error" class="mr-4 mt-3 mb-3" @click="reset">
              Limpiar formulario
            </v-btn >
            </v-container>
          </v-card>
        </v-form>
      </v-col>
      <v-col cols="12">
        <v-divider color="black"/>
      </v-col>
      <div v-if="Show == true && this.next == true">
        <h1 class="mt-3 mb-3">
          Resultado obtenido usando algoritmo {{this.Algoritmo}} con {{this.J}} datos
          <v-carousel cycle show-arrows-on-hover hide-delimiter-background>
            <v-carousel-item v-for="(r,index) in response" :key="index">
              <v-col justify="center" align="center" cols="12">
                <v-hover v-slot:default="{ hover }">
                <v-card 
                :elevation="hover ? 24 : 4"
                class="blue lighten-3 mt-3 mb-3" color="white" >
                  <v-card-title class=" justify-center">
                  <h1 class="display-1 font-weight-medium">
                    {{r[0][0][0]}}
                    </h1>
                  </v-card-title>
                  <img v-bind:src="'data:image/png;base64,'+r[1]" />
                  <v-col cols="5">
                    <v-divider color="white"/>
                    <v-divider color="white"/>
                  </v-col>
                  <v-card-text> 
                    <v-col cols="12" v-if="K > 0">
                      <h1 class="subtitle-1 font-weight-bold">
                        Apareció {{r[0][0][1]}} veces de {{K}}
                      </h1>
                      <h1 class="subtitle-1 font-weight-bold">
                        Tiempo de ejecucion: {{r[0][1]}} segundos
                      </h1>  
                    </v-col>
                    <v-col cols="12" v-if="R > 0">
                      <h1 class="subtitle-1 font-weight-bold">
                        Apareció {{r[0][0][1]}} veces usando radio {{R}}
                      </h1>
                      <h1 class="subtitle-1 font-weight-bold">
                        Tiempo de ejecucion: {{r[0][1]}} segundos
                      </h1>  
                    </v-col>
                  </v-card-text>
                </v-card>
                </v-hover>
              </v-col>
            </v-carousel-item>
          </v-carousel>      
        </h1>  
      </div>  
    </v-row>
  </v-container>
</template>

<script>

export default {
  name: 'Home',
  data: ()=>({
    valid:true,
    dis:false,
    Show:false,
    image:[
    ],
    Algoritmos:[
      'KNN-Rtree',
      'KNN-Sequential',
      'Range Search-RTree'
    ],
    Algoritmo:'',
    K:'',
    R:'',
    Porcentaje:'',
    P:0,
    J:0,
    fileRules: [
      v => !!v || 'Imagen requerida'
    ],
    response:[],
    next:false,
    Valores_p: [
      '100',
      '200',
      '400',
      '800',
      '1600',
      '3200',
      '6400',
      '13171'
    ],
  }),
  computed:{
    color () {
        if (this.P <4) return 'red'
        return 'green'
      },
  },
  methods:{
    decrement () {
      this.P--
    },
    increment () {
      this.P++
    },
    async cargar(){
      //console.log(this.image);
      const form = new FormData();
      form.append('file',this.image);
      form.append('Algoritmo',this.Algoritmo);
      form.append('K',this.K);
      form.append('R',this.R);
      
      switch(this.P){
        case 0:
          this.P = 100;
          break;
        case 1:
          this.P = 200;
          break;
        case 2:
          this.P = 400;
          break;
        case 3:
          this.P = 800; 
          break;     
        case 4:
          this.P = 1600;
          break;
        case 5:
          this.P = 3200;
          break;
        case 6:
          this.P = 6400;
          break;
        case 7:
          this.P = 13171;
          break;
        default:
          this.P = 0;
          break;
      }
      this.J = this.P;
      form.append('P',this.P);

      if(this.K == ""){
        this.K = 0;
      }else{
        this.R = 0;
      }

      this.response = await this.$store.dispatch('Post_image',form);
      if(this.response.error){
        alert(this.response.error)
      }else{
        alert('Datos enviados correctamente')
        this.next = true;
      }  
      this.Show = true,
      this.dis = true,
      this.valid = false;
      
      for (var i = 0; i < (this.response.length); i++) {
        this.response[i][0][0][0] = this.response[i][0][0][0].replace("_", " ");
        this.response[i][0][1] = parseFloat(this.response[i][0][1]).toFixed(4)
      }
      return this.response
    },
    reset () {
      this.$refs.form.reset()
      this.Show = false,
      this.dis = false
      this.K = ''
      this.R = ''
    }
  }
}
</script>
