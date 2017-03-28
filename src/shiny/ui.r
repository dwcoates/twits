library(shiny)

# Create Input controls
day = Slider(title="Day", value=0, start=0, end=7, step=1)
retweets = Slider(title="Retweets", value=0, start=0, end=7, step=1)

# Define UI for application that draws a histogram
fluidPage(

  # Application title
  titlePanel("Hello Shiny!"),

  # Sidebar with a slider input for the number of bins
  sidebarLayout(
    sidebarPanel(
      sliderInput("day",
                  "Day between Jan 28th and Feb 17th:",
                  min = 1,
                  max = 31,
                  value = 1),
      sliderInput("retweets",
                  "Max number of retweets:",
                  min = 1,
                  max = 30000,
                  value = 1)
    ),
    # Show a plot of the generated distribution
    mainPanel(
      plotOutput("distPlot")
    )
  )
)

