library(shiny)

fluidPage(
  titlePanel("Retweets by day"),

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
                  max = 1000,
                  value = 1)
    ),
    # Show a plot of the generated distribution
    mainPanel(
      plotOutput("distPlot")
    )
  )
)

