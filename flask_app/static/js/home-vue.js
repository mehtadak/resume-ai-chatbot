// Home Vue Component
const HomeComponent = {
  template: `
    <div id="home-app" class="max-w-6xl mx-auto">
      <!-- Hero Section -->
      <div class="text-center mb-16">
      </div>

      <!-- Main Content -->
      <div class="bg-white rounded-lg shadow-lg overflow-hidden mb-12">
        <div class="flex">
          <div class="w-1/3 p-8 flex items-center justify-center bg-gray-200">
            <img src="/static/images/headshot.png" alt="Daksh Mehta" class="w-64 h-64 rounded-full object-cover shadow-lg">
          </div>
          <div class="w-2/3 p-8">
            <h2 class="text-3xl font-bold text-gray-900 mb-6">About me:</h2>
            <div class="prose prose-lg text-gray-700 space-y-4">
              <p>
                <span class="font-semibold text-gray-700">Daksh Mehta</span>
                is a third-year Computer Science student at Michigan State University, where he is also pursuing a minor in Game Development. His academic excellence has been recognized with repeated placements on the Dean’s List and the International Student Scholarship. Daksh combines a strong technical foundation with a passion for building impactful, data-driven solutions and interactive experiences. 
              </p>
              <p>
                Professionally, Daksh has gained hands-on experience through his internship at iCustomer, where he worked on data pipelines, automation workflows, and API integrations. He has also developed projects ranging from OpenGL-based graphics applications to Unity game prototypes, showcasing both his problem-solving skills and creativity. His technical expertise spans C++, Python, SQL, Unity, OpenGL, and modern data analysis practices.
              </p>
              <p>
                Daksh is particularly interested in the intersection of data, business intelligence, and technology-driven storytelling. He thrives in collaborative environments where curiosity, design thinking, and technical rigor come together to solve complex problems. Looking ahead, he aspires to leverage his skills in data engineering, visualization, and intelligent systems to create innovative tools that empower people and organizations.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- What You'll Get Out of This Class Section -->
      <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-lg overflow-hidden mb-12">
        <div class="p-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-8 text-center">What I Hope You'll Get From This Class:</h2>
          
          <div class="grid grid-cols-3 gap-8">
            <!-- Technical Skills -->
            <div class="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
              <div class="text-gray-600 mb-4 text-center">
                <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-3 text-center">Technical Skills</h3>
              <p class="text-gray-600 text-center">Learn the fundamentals of AI agent development, including LLMs, RAG, and more.</p>
            </div>

            <!-- Practical Experience -->
            <div class="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
              <div class="text-gray-600 mb-4 text-center">
                <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-3 text-center">Practical Experience</h3>
              <p class="text-gray-600 text-center">Build real-world AI agents through hands-on projects, gaining experience with tools and frameworks used in industry.</p>
            </div>

            <!-- Problem-Solving Skills -->
            <div class="bg-white rounded-lg p-6 shadow-md hover:shadow-lg transition-shadow duration-300">
              <div class="text-gray-600 mb-4 text-center">
                <svg class="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-3 text-center">Problem-Solving Skills</h3>
              <p class="text-gray-600 text-center">Develop critical thinking and analytical skills to tackle complex AI challenges and design intelligent solutions.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,

  setup() {
    // Add your reactive state and methods for AI agent features here
    
    return {
      // Return any reactive variables or methods you add
    };
  }
};

// Use the shared Vue utilities for initialization
VueAppFactory.createApp(HomeComponent, 'home-container', 'Home App');
